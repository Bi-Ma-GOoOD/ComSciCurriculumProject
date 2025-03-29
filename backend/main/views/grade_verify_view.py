import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from ..services import GradeVerificationService as GV

gv = GV()

class GradeVerifyView(APIView) :
    def get(self, request) :        
        data = request.query_params.get('uid')
        if data :
            try :
                
                response, isGraduateCheck = gv.getVerification(data)
                
                return Response(
                    {
                        'success':True,
                        'is_graduate_check': isGraduateCheck,
                        'message': response,
                    },
                    status=HTTP_200_OK,
                )
            
            except Exception as e :
                print('\n------------------')
                print('Exception occor:', e)
                return Response(
                    {
                        'success': False,
                        'message': 'เกิดข้อผิดพลาดจากผลลัพธ์การคำนวณ',
                    },
                    status=HTTP_400_BAD_REQUEST,
                )
        
        return Response(
            {
                'success': False,
                'message': 'uid is required',
            },
            status=HTTP_400_BAD_REQUEST,
        )
        
    def delete(self, request) :
        uid = request.query_params.get('uid')
        print('uid:', uid)
        
        if uid :
            try :
                response = gv.deleteVerification(uid)
                return Response(
                    {
                        'success': True,
                        'message': response,
                    },
                    status=HTTP_200_OK,
                )
            except Exception as e :
                return Response(
                    {
                        'success': False,
                        'message': 'เกิดข้อผิดพลาดจากการลบข้อมูล',
                    },
                    status=HTTP_400_BAD_REQUEST,
                )
                
        else :
            return Response(
                {
                    'success': False,
                    'message': 'uid is required',
                },
                status=HTTP_400_BAD_REQUEST,
            )
            
            
            
            

