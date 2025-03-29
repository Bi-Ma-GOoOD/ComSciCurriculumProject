import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from ..services import EducationEvaluationService as EES

ees = EES()

class CalculateView(APIView):
    def post(self, request):
        uid = request.query_params.get('uid')
        if uid :
            try :
              
                response = ees.verify(
                    userId=uid,
                )
                    
                return Response(
                    {
                        'success':True,
                        'data': response,
                    },
                    status=HTTP_200_OK,
                )
            
            except Exception as e :
                print('\n------------------')
                print('Exception occor:', e)
                return Response(
                    {
                        'success': False,
                        'message': 'เกิดข้อผิดพลาดจากการคำนวณผลลัพธ์',
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