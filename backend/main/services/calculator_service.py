from typing import Dict, List
from ortools.linear_solver import pywraplp

from ..utils import utils
from ..serializers import CreditVerifySerializer
from ..models import Enrollment, Curriculum, Subcategory, CaluculatedEnrollment

from ..utils import utils

class CalculatorService() :
    def __init__(self):
        pass
    
    def __str__(self):
        pass
    
    def GPACalculate(self, stEnrollments: List[Enrollment]) -> List[Enrollment] :
        """calculate final gpa for duplicate subject

        Args:
            stEnrollments (List[Enrollment]): study result for each student (with duplicate course)

        Returns:
            List[Enrollment]: final study result grade (with no duplicate course)
        """
        
        calculatedEnrollments :Dict[str, CaluculatedEnrollment] = {}
        encounter :Dict[str, int] = {}
        
        for enrollment in stEnrollments :
            key = enrollment.course_fk.course_id
            newGrade, charGrade = utils.getGrade(enrollment.grade)
            if calculatedEnrollments.get(key) :
                # if duplicate course will add total grade
                if newGrade != None :
                    calculatedEnrollments[key].totalGrade += newGrade
                    calculatedEnrollments[key].charGrade = None
                
                # DONE:  implement update recently year and semester
                if enrollment.year > calculatedEnrollments[key].enrollment.year :
                    calculatedEnrollments[key].enrollment.year = enrollment.year
                    calculatedEnrollments[key].enrollment.semester = enrollment.semester
                elif enrollment.semester == Enrollment.Semester.SECOND :
                    calculatedEnrollments[key].enrollment.year = enrollment.year
                    calculatedEnrollments[key].enrollment.semester = enrollment.semester
                elif enrollment.semester == Enrollment.Semester.FIRST :
                    calculatedEnrollments[key].enrollment.year = enrollment.year
                    calculatedEnrollments[key].enrollment.semester = enrollment.semester
                else :
                    raise RuntimeError("should not study the same subject in the same semester and year")
                
            else :
                # if first encounter add fresh data
                calculatedEnrollments[key] = CaluculatedEnrollment(
                    enrollment=enrollment,
                    totalGrade=newGrade,
                    charGrade=charGrade,
                )
                
                encounter[key] = 0
            
            if newGrade != None :
                # increment if grade not None
                encounter[key] += 1
            
        # averaging the gpa for every courses
        for key in list(calculatedEnrollments.keys()) :
            if calculatedEnrollments[key].totalGrade != None :
                calculatedEnrollments[key].totalGrade /= encounter[key]
            
        return list(calculatedEnrollments.values())
        
    def map(self, subcategories: List[Subcategory], enrollments: List[CaluculatedEnrollment]) :
        """mapping and categorize the studied courses to categories

        Args:
            subcategories (List[Subcategory]): all category from course curriculum
            enrollments (List[Enrollment]): all studied course of user

        Returns:
            map[str, List]: object of {free elective, categorize courses}
        """
        
        result = {'free elective': [], 'categorize course': []}
        
        mappedEnrollments = self.categorizeSubject(subcategories=subcategories, enrollments=enrollments)
        
        # วิชา 5 กลุ่มสาระ
        for universitySubcate in utils.UNIVERSITY_SUBCATEGORY :
            if not mappedEnrollments.get(utils.FIVE_UNIVERSITY_SUBCATEGORY) :
                continue
            
            data = mappedEnrollments[universitySubcate]
            if data['subcategory'].subcateory_min_credit < data['sumCredit'] :
                
                print('\n----------------------- 5 กลุ่มสาระ -----------------------')
                
                formatedData = {course.enrollment.course_fk.course_id: self.convertEnrollment(course) for course in data['matchEnrollment'].values()}
                optimalAns = self.optimization('SAT', formatedData, data['subcategory'].subcateory_min_credit)
                
                if not optimalAns :
                    optimalAns = self.optimization('GLOP', formatedData, data['subcategory'].subcateory_min_credit)
                    
                for courseId, selection in optimalAns :
                    if selection == 0 :
                        removedCourse = data['matchEnrollment'].pop(courseId)
                        data['sumCredit'] -= removedCourse.enrollment.course_fk.credit
                        
                        mappedEnrollments[utils.FIVE_UNIVERSITY_SUBCATEGORY]['matchEnrollment'][removedCourse.enrollment.course_fk.course_id] = removedCourse
                        mappedEnrollments[utils.FIVE_UNIVERSITY_SUBCATEGORY]['sumCredit'] += removedCourse.enrollment.course_fk.credit
            
        # วิชาเลือกเสรี
        for mappedEnrollment in mappedEnrollments.values() :            
            if mappedEnrollment['subcategory'].subcateory_min_credit < mappedEnrollment['sumCredit'] :
                # เกลี่ยรายวิชา
                print('\n----------------------- วิชาเลือกเสรี -----------------------')
                
                formatedData = {course.enrollment.course_fk.course_id: self.convertEnrollment(course) for course in mappedEnrollment['matchEnrollment'].values()}
                optimalAns = self.optimization('SAT', formatedData, mappedEnrollment['subcategory'].subcateory_min_credit)
                
                if not optimalAns :
                    optimalAns = self.optimization('GLOP', formatedData, mappedEnrollment['subcategory'].subcateory_min_credit)
                    
                for courseId, selection in optimalAns :
                    if selection == 0 :
                        removedCourse = mappedEnrollment['matchEnrollment'].pop(courseId)
                        mappedEnrollment['sumCredit'] -= removedCourse.enrollment.course_fk.credit
                        
                        result['free elective'].append(removedCourse)

            result['categorize course'].append(mappedEnrollment)
            
        for enrollment in enrollments :
            if enrollment.enrollment.course_fk.subcategory_fk is None :
                result['free elective'].append(enrollment)
                        
        return result
    
    def categorizeSubject(self, subcategories: List[Subcategory], enrollments: List[CaluculatedEnrollment]) -> map :
        """categorize the studied courses match with subcategories

        Args:
            subcategories (List[Subcategory]): subcategories from course curriculum
            enrollments (List[Enrollment]): studied courses of user

        Raises:
            RuntimeError: user have been studied in course that not in user's curriculum year

        Returns:
            map: group of {subcategory, match courses, total credit}
        """
        
        mappedEnrollments = {
            subcategory.subcategory_name: {'subcategory': subcategory, 'matchEnrollment':{}, 'sumCredit':0} for subcategory in subcategories
        }
        
        for enrollment in enrollments :
            if enrollment.enrollment.course_fk.subcategory_fk is None :
                continue
            
            subcategoryName = enrollment.enrollment.course_fk.subcategory_fk.subcategory_name
            matchSubcategory = mappedEnrollments.get(subcategoryName)
            
            if matchSubcategory :
                matchSubcategory['matchEnrollment'][enrollment.enrollment.course_fk.course_id] = enrollment
                matchSubcategory['sumCredit'] += enrollment.enrollment.course_fk.credit
            else :
                raise RuntimeError('inserted enrollment got unexpexted subject or category')

        return mappedEnrollments
        
    def convertEnrollment(self, enrollment: CaluculatedEnrollment) -> map :
        """grouping data of studied course

        Args:
            enrollment (Enrollment): studied course of user

        Returns:
            map: data mapping object
        """
        
        return {
            'enrollment': enrollment,
            'credit': enrollment.enrollment.course_fk.credit,
            'courseId': enrollment.enrollment.course_fk.course_id,
        }
        
    def optimization(self, model: str, convertedEnrollment: map, minCredit: int) -> List[tuple[str, int]]|None :
        """to optimize fitting studied course to the curriculum category

        Args:
            model (str): SAT (integer solver), GLOP (linear solver)
            convertedEnrollment (map): studied course data
            minCredit (int): minimum credit must take in curriculum course

        Returns:
            List[tuple[str, int]]|None: (course, decision) is telling that course will be choose to be in subcategory or None if problem not feasible
        """
        
        # linear programming solver
        solver: pywraplp.Solver = pywraplp.Solver.CreateSolver(model)
        
        # variable
        variables = []
        for enrollment in convertedEnrollment.values() :
            if isinstance(enrollment['enrollment'].totalGrade, float) :
                variable = solver.IntVar(0, 1, enrollment['enrollment'].enrollment.course_fk.course_id)
                variables.append(variable)
        
        # constraint
        constraint = sum([v*convertedEnrollment[v.name()]['credit'] for v in variables])
        print('\n-----------------------')
        print('Constraint:', constraint)
        
        solver.Add(constraint == minCredit)
        
        # objective   
        objective = sum([v for v in variables])
        solver.Maximize(objective)
        
        status = solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL :
            for v in variables :
                print(f"{v.name()} = {v.solution_value():0.1f}")
                
            return [(v.name(), round(v.solution_value())) for v in variables]
                
        else :
            print('problem not feasible')
            return None