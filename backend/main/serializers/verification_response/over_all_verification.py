from rest_framework import serializers

from .study_verification_serializer import StudyVerificationSerializer  # Adjust the import path as necessary

class OverallVerificationSerializer(serializers.Serializer):
    
    def to_representation(self, instance):
        if not (
            isinstance(instance.get('studyResult'), dict) and
            isinstance(instance.get('feeResult'), int) and
            isinstance(instance.get('activityResult'), int)
            ) :
            raise Exception("Invalid instance format: 'studyResult' must be a dict, 'feeResult' and 'activityResult' must be integers.")
            
        return {
            'fee_result': bool(instance.get('feeResult')),
            'activity_result': bool(instance.get('activityResult')),
            'study_result': self.getStudyResult(instance.get('studyResult'))
        }
        
    def getStudyResult(self, obj) :
        return StudyVerificationSerializer(obj).data