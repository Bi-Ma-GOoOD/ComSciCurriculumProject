import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from ..utils.mock_data import *
from ..services import GradeVerificationService as GV

gv = GV()

class GradeVerifyView(APIView) :
    def get(self, request) :        
        data = request.GET.get('uid')
        if data :
            try :
                
                response = gv.getVerification(data)
                return Response(response, status=HTTP_200_OK)
            
            except Exception as e :
                print('\n------------------')
                print('Exception occor:', e)
                return Response(e, status=HTTP_400_BAD_REQUEST)
        
        return Response(status=HTTP_400_BAD_REQUEST)
            
            
            
            

