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
                
                with open('output1.txt', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(response, ensure_ascii=False, indent=4))
                
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
                        'message': str(e),
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
                        'message': str(e),
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
            
            
            
            

