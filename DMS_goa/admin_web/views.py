from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from .permissions import IsAdmin, IsManager, IsERO
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework import status
from admin_web.renders import UserRenderer
from django.contrib.auth import authenticate
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from geopy.geocoders import Nominatim
import ast

class DMS_department_post_api(APIView):
    def post(self,request):
        serializers=DMS_department_serializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST) 

class DMS_department_put_api(APIView):
    def get(self, request, dep_id):
        snippet = DMS_Department.objects.filter(dep_id=dep_id,dep_is_deleted=False)
        serializers = DMS_department_serializer(snippet, many=True)
        return Response(serializers.data)

    def put(self, request, dep_id):
        try:
            instance = DMS_Department.objects.get(dep_id=dep_id)
        except DMS_Department.DoesNotExist:
            return Response({"error": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DMS_department_serializer(instance, data=request.data, partial=True)  # partial=True allows partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DMS_department_delete_api(APIView):
    def get(self, request, dep_id):
        try:
            instance = DMS_Department.objects.get(dep_id=dep_id, dep_is_deleted=False)
        except DMS_Department.DoesNotExist:
            return Response({"error": "Department not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DMS_department_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, dep_id):
        try:
            instance = DMS_Department.objects.get(dep_id=dep_id, dep_is_deleted=False)
        except DMS_Department.DoesNotExist:
            return Response({"error": "Department not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)

        instance.dep_is_deleted = True
        instance.save()
        return Response({"message": "Department soft deleted successfully."}, status=status.HTTP_200_OK)

class DMS_Group_post_api(APIView):
    def post(self,request):
        serializers=DMS_Group_serializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST) 

class DMS_Group_put_api(APIView):
    def get(self, request, grp_id):
        snippet = DMS_Group.objects.filter(grp_id=grp_id,grp_is_deleted=False)
        serializers = DMS_Group_serializer(snippet, many=True)
        return Response(serializers.data)

    def put(self, request, grp_id):
        try:
            instance = DMS_Group.objects.get(grp_id=grp_id)
        except DMS_Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DMS_Group_serializer(instance, data=request.data, partial=True)  # partial=True allows partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DMS_Group_delete_api(APIView):
    def get(self, request, grp_id):
        try:
            instance = DMS_Group.objects.get(grp_id=grp_id, grp_is_deleted=False)
        except DMS_Group.DoesNotExist:
            return Response({"error": "Group not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DMS_Group_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, grp_id):
        try:
            instance = DMS_Group.objects.get(grp_id=grp_id, grp_is_deleted=False)
        except DMS_Group.DoesNotExist:
            return Response({"error": "Group not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)

        instance.grp_is_deleted = True
        instance.save()
        return Response({"message": "Group soft deleted successfully."}, status=status.HTTP_200_OK)

class DMS_Employee_get_api(APIView):
    def get(self,request):
        snippet = DMS_Employee.objects.filter(emp_is_deleted=False).order_by('-emp_added_date')
        serializers = DMS_Employee_GET_serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class DMS_Employee_post_api(APIView):
    def post(self,request):
        serializers=DMS_Employee_serializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST) 
    

class DMS_Employee_Idwise_get_api(APIView):
    def get(self,request,emp_id):
        snippet = DMS_Employee.objects.filter(emp_is_deleted=False,emp_id=emp_id).order_by('-emp_added_date')
        serializers = DMS_Employee_GET_serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class DMS_Employee_put_api(APIView):
    def get(self, request, emp_id):
        snippet = DMS_Employee.objects.filter(emp_id=emp_id,emp_is_deleted=False)
        serializers = DMS_Employee_GET_serializer(snippet, many=True)
        return Response(serializers.data)

    def put(self, request, emp_id):
        try:
            instance = DMS_Employee.objects.get(emp_id=emp_id)
        except DMS_Employee.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DMS_Employee_serializer(instance, data=request.data, partial=True)  # partial=True allows partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DMS_Employee_delete_api(APIView):
    def get(self, request, emp_id):
        try:
            instance = DMS_Employee.objects.get(emp_id=emp_id, emp_is_deleted=False)
        except DMS_Employee.DoesNotExist:
            return Response({"error": "Employee not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DMS_Employee_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, emp_id):
        try:
            instance = DMS_Employee.objects.get(emp_id=emp_id, emp_is_deleted=False)
        except DMS_Employee.DoesNotExist:
            return Response({"error": "Employee not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)

        instance.emp_is_deleted = True
        instance.save()
        return Response({"message": "Employee soft deleted successfully."}, status=status.HTTP_200_OK)

 
class DMS_state_get_api(APIView):
    
    def get(self,request):
        snippet = DMS_State.objects.filter(state_is_deleted=False)
        serializers = DMS_State_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class DMS_state_idwise_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,state_id):
        snippet = DMS_State.objects.filter(state_id=state_id,state_is_deleted=False)
        serializers = DMS_State_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
class DMS_district_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        snippet = DMS_District.objects.filter(dis_is_deleted=False)
        serializers = DMS_District_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class DMS_district_idwise_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,state_id):
        snippet = DMS_District.objects.filter(state_id=state_id,dis_is_deleted=False)
        serializers = DMS_District_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class DMS_Tahsil_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        snippet = DMS_Tahsil.objects.filter(tah_is_deleted=False)
        serializers = DMS_Tahsil_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)   


class DMS_Tahsil_idwise_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,dis_id):
        snippet = DMS_Tahsil.objects.filter(dis_id=dis_id,tah_is_deleted=False)
        serializers = DMS_Tahsil_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
class DMS_City_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        snippet = DMS_City.objects.filter(cit_is_deleted=False)
        serializers = DMS_City_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class DMS_City_idwise_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,tah_id):
        snippet = DMS_City.objects.filter(tah_id=tah_id,cit_is_deleted=False)
        serializers = DMS_City_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class DMS_Group_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        snippet = DMS_Group.objects.filter(grp_is_deleted=False).order_by('-grp_added_date')
        serializers = DMS_Group_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
class DMS_Group_idwise_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,grp_id):
        snippet = DMS_Group.objects.filter(grp_id=grp_id,grp_is_deleted=False)
        serializers = DMS_Group_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
class DMS_Department_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        snippet = DMS_Department.objects.filter(dep_is_deleted=False)
        serializers = DMS_Department_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
class DMS_Department_idwise_get_api(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,dep_id):
        snippet = DMS_Department.objects.filter(dep_id=dep_id,dep_is_deleted=False)
        serializers = DMS_Department_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
 


# class CaptchaTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CaptchaTokenObtainPairSerializer


class CaptchaAPIView(APIView):
    def get(self, request):
        new_captcha = CaptchaStore.generate_key()
        image_url = captcha_image_url(new_captcha)
        return Response({
            'captcha_key': new_captcha,
            'captcha_image_url': image_url,
        })



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    group = str(user.grp_id.grp_id)
    print("user---123", user)
    print("group---123", user.grp_id.grp_id)
    # permissions_data = []
    # if group:
    #     incs= DMS_Group.objects.get(grp_id=group)
    #     pers = DMS_Permission.objects.filter(grp_id=group)
    #     group_id = incs.grp_id
    #     for permission in pers:
    #         permission_info = {
    #             'modules_submodule': permission.mod_submod_per,
    #             'permission_status': permission.per_is_deleted,
    #             # 'source_id': permission.source.source_pk_id,
    #             # 'source_name': permission.source.source,  
    #             'group_id': permission.grp_id.grp_id,
    #             'group_name': permission.grp_id.grp_name,  
    #         }   
    #         permissions_data.append(permission_info)
    # else:
    #     group = None
            
    return {
        "refresh" : str(refresh),
        "access" : str(refresh.access_token),
        # "permissions": permissions_data,
        "colleague": {
                'id': user.emp_id,
                'emp_name': user.emp_name,
                'email': user.emp_email,
                'phone_no': user.emp_contact_no,
                'user_group': group,
            },
        "user_group" :group,
    } 


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        # Validate using the CAPTCHA + credential serializer
        serializer1 = CaptchaTokenObtainPairSerializer(data=request.data)
        serializer1.is_valid(raise_exception=True)


        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            emp_username = serializer.data.get('emp_username')
            password = serializer.data.get('password')
            print("=========", emp_username, password)
            user = authenticate(emp_username=emp_username, password=password)
            print("user--", user)
            if user is not None:
                emp = DMS_Employee.objects.get(emp_username=user.emp_username)
                if emp.emp_is_deleted != False:
                    return Response({'msg':'Login access denied. Please check your permissions or reach out to support for help.'},status=status.HTTP_401_UNAUTHORIZED)
                if emp.emp_is_login is False: 
                    emp.emp_is_login = True
                    emp.save()
                    token = get_tokens_for_user(user)
                    return Response({'token':token,'msg':'Logged in Successfully'},status=status.HTTP_200_OK)
                else:
                    return Response({'msg':'User Already Logged In. Please check.'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['UserId or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can log out

    def post(self, request):
        try:
            print("1", request.user)
            emp_obj = DMS_Employee.objects.get(emp_username=request.user)
            if emp_obj.emp_is_login is True: 
                emp_obj.emp_is_login = False
                emp_obj.save()
                
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the token
                return Response({"message": "Logged out successfully"}, status=200)
            return Response({"error": "Refresh token is required"}, status=400)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)
        
        
class CombinedAPIView(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        permission_modules = DMS_Module.objects.filter()
        modules_serializer = Mmoduleserializer(permission_modules, many=True)

        permission_objects = DMS_SubModule.objects.filter()
        permission_serializer = permission_sub_Serializer(permission_objects, many=True)

        
        combined_data = []
        for module_data in modules_serializer.data:
            module_id = module_data["mod_id"]
            module_name = module_data["mod_name"]
            group_id = module_data["mod_group_id"]
            group_name = module_data["grp_name"]
            

            submodules = [submodule for submodule in permission_serializer.data if submodule["mod_id"] == module_id]

            formatted_data = {
                "group_id": group_id,
                "group_name": group_name,
                "module_id": module_id,
                "name": module_name,
                "submodules": submodules
            }

            combined_data.append(formatted_data)

        final_data = combined_data

        return Response(final_data)


    
    
class DMS_Group_put_api(APIView):
    def get(self, request, grp_id):
        snippet = DMS_Group.objects.filter(grp_id=grp_id,grp_is_deleted=False)
        serializers = DMS_Group_Serializer(snippet, many=True)
        return Response(serializers.data)

    def put(self, request, grp_id):
        try:
            instance = DMS_Group.objects.get(grp_id=grp_id)
        except DMS_Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DMS_Group_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DMS_ChangePassword_put_api(APIView):
    def get(self, request, emp_id):
        snippet = DMS_Employee.objects.filter(emp_id=emp_id,emp_is_deleted=False)
        serializers = ChangePasswordGetSerializer(snippet, many=True)
        return Response(serializers.data)

    def put(self, request, emp_id):
        try:
            instance = DMS_Employee.objects.get(emp_id=emp_id)
        except DMS_Employee.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChangePasswordputSerializer(instance, data=request.data, partial=True)  # partial=True allows partial updates


        plain_password = request.data['password']
        hashed_password = make_password(plain_password)
        print("++++++++", hashed_password, plain_password)
        request.data['password'] = hashed_password
        request.data['password2'] = hashed_password
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DMS_ChangePassword_api(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("here--------------------")
        serializer = ChangePasswordSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if not user.check_password(old_password):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class DMS_ForgotPassword_api(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = DMS_Employee.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"
            # Or send as POST URL: /api/accounts/reset-confirm/{uid}/{token}/

            send_mail(
                "Password Reset",
                f"Click the link to reset your password: {reset_link}",
                "noreply@yourapp.com",
                [email],
                fail_silently=False,
            )
            return Response({"detail": "Password reset link sent."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# accounts/views.py
class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        data = {
            "uid": uid,
            "token": token,
            "new_password": request.data.get("new_password"),
        }
        serializer = PasswordResetConfirmSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password has been reset successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DMS_Sop_get_api(APIView):
    def get(self,request):
        snippet = DMS_SOP.objects.filter(sop_is_deleted=False)
        serializers = SopSerializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class DMS_Sop_post_api(APIView):
    def post(self, request):
        disaster_id = request.data.get('disaster_id')

        if disaster_id is None:
            return Response({"error": "disaster_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        existing = DMS_SOP.objects.filter(disaster_id=disaster_id, sop_is_deleted=False).first()
        
        if existing:
            return Response(
                {"error": "SOP for this disaster_id already exists."},
                status=status.HTTP_409_CONFLICT
            )
        
        serializer = SopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DMS_Sop_put_api(APIView):
    def get(self, request, sop_id):
        snippet = DMS_SOP.objects.filter(sop_id=sop_id)
        serializers = SopSerializer(snippet, many=True)
        return Response(serializers.data)

    def put(self, request, sop_id):
        try:
            instance = DMS_SOP.objects.get(sop_id=sop_id)
        except DMS_SOP.DoesNotExist:
            return Response({"error": "Sop not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = Sop_Put_Serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class DMS_Sop_delete_api(APIView):
    def get(self, request, sop_id):
        try:
            instance = DMS_SOP.objects.get(sop_id=sop_id, sop_is_deleted=False)
        except DMS_SOP.DoesNotExist:
            return Response({"error": "Sop not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SopSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, sop_id):
        try:
            instance = DMS_SOP.objects.get(sop_id=sop_id, sop_is_deleted=False)
        except DMS_SOP.DoesNotExist:
            return Response({"error": "Sop not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)

        instance.sop_is_deleted = True
        instance.save()
        return Response({"message": "Sop soft deleted successfully."}, status=status.HTTP_200_OK)

 
class DMS_Disaster_Type_Get_API(APIView):
    def get(self,request):
        snippet = DMS_Disaster_Type.objects.filter(disaster_is_deleted=False)
        serializers = DMS_Disaster_Type_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class DMS_Disaster_Type_Idwise_Get_API(APIView):
    def get(self,request,disaster_id):
        snippet = DMS_Disaster_Type.objects.filter(disaster_is_deleted=False,disaster_id=disaster_id)
        serializers = DMS_Disaster_Type_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    

class DMS_Alert_idwise_get_api(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        print("request user-- ",request.user)
        alert_id = request.GET.get('id')
        st = request.GET.get('st')
        if alert_id and st == 1:
            print("1")
            alert_obj = Weather_alerts.objects.get(pk_id=alert_id)
            alert_obj.triger_status = 1
            alert_obj.modified_by = str(request.user)
            alert_obj.save()
            print("done")
        else:
            print("2")
            alert_obj = Weather_alerts.objects.get(pk_id=alert_id)
            alert_obj.triger_status = 2
            alert_obj.modified_by = str(request.user)
            alert_obj.save()
            print("done 2")
        serializers = WeatherAlertSerializer(alert_obj,many=False)
        return Response(serializers.data, status=status.HTTP_200_OK)
    

class DMS_Incident_Post_api(APIView):
    def post(self,request):
        serializers=Incident_Serializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            print(serializers.data.get('inc_id'))
            alert_id = request.data['alert_id']
        
            # Initialize the geocoder
            geolocator = Nominatim(user_agent="nikita.speroinfosystems@gmail.com")

            if alert_id:
                try:
                    weather_obj = Weather_alerts.objects.get(pk_id=alert_id)
                    weather_obj.triger_status = 3
                    weather_obj.save()
                    print(f"Weather_alerts updated: triger_status set to 3 for alert_id {alert_id}")
                except Weather_alerts.DoesNotExist:
                    print(f"Weather_alerts with pk_id={alert_id} not found")

                Inc_obj = DMS_Incident.objects.filter(alert_id=alert_id).last()
                print("inc obj-", Inc_obj)

                if Inc_obj:
                    latitude = Inc_obj.latitude
                    longitude = Inc_obj.longitude

                    # Reverse geocoding
                    location = geolocator.reverse((latitude, longitude), language='en')
                    print("location.address---", location.address)

                    Inc_obj.location = location.address
                    Inc_obj.save()

            sinc = serializers.data.get('inc_id')
            incc = DMS_Incident.objects.get(inc_id=sinc)

            external_api_payload = {
                "caller_name": "",
                "caller_no": "",
                "location": "",
                "summary": "",
                "disaster_name": incc.disaster_type.disaster_name if incc.disaster_type else None,
                "inc_type": incc.disaster_type.disaster_id if incc.disaster_type else None,
                "incident_id": str(incc.incident_id),
                "latitude": str(incc.latitude),
                "longitude": str(incc.longitude),
                "dms_lat": str(incc.latitude),
                "dms_lng": str(incc.longitude),
                "alert_type": ("High" if incc.alert_type == 1 else"Medium" if incc.alert_type == 2 else"Low" if incc.alert_type == 3 else"Very Low" if incc.alert_type == 4 else"")
            } 
            print(external_api_payload)
            external_response = requests.post(
                "http://210.212.165.119/Spero_DMS/dms/alert_details",
                json=external_api_payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if external_response.status_code == 200:
                external_api_result = external_response.json()
            else:
                external_api_result = {
                    "error": f"Status {external_response.status_code}",
                    "response": external_response.text
                }
            aaa = DMS_Comments.objects.filter(incident_id=incc).last()
            nn = {"incident_id": incc.incident_id,"alert_comment": aaa.comments}
            external_response = requests.post(
                    "http://210.212.165.119/Spero_DMS/dms/alert_comments",
                    json=nn,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
            print(external_response.json())

            data = {
                "sr_dt":serializers.data,
                "external_api_result":external_api_result
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            print("hiiiiiii else")
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)





class DMS_Comments_Post_api(APIView):
    def post(self,request):
        serializers=Comments_Serializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class alerts_get_api(APIView):
    def get(self, request, disaster_id):
        sop_responses = DMS_SOP.objects.filter(disaster_id=disaster_id)
        sop_serializer = Sop_Response_Procedure_Serializer(sop_responses, many=True)
        return Response(sop_serializer.data, status=status.HTTP_200_OK)
    
    
# class Manual_Call_Incident_api(APIView):
#     def post(self, request, *args, **kwargs):
#         data = request.data

#         incident_fields = [
#             'inc_type', 'disaster_type', 'alert_type', 'location', 'summary',
#             'responder_scope', 'latitude', 'longitude', 'caller_id',
#             'inc_added_by', 'inc_modified_by', 'incident_id', 'inc_id','time','mode',
#         ]
#         caller_fields = ['caller_no', 'caller_name', 'caller_added_by', 'caller_modified_by']
#         comments_fields = ['comments', 'comm_added_by', 'comm_modified_by']

#         incident_data = {field: data.get(field) for field in incident_fields}
#         caller_data = {field: data.get(field) for field in caller_fields}
#         comments_data = {field: data.get(field) for field in comments_fields}

#         # Step 1: Save caller
#         caller_serializer = Manual_call_data_Serializer(data=caller_data)
#         if not caller_serializer.is_valid():
#             return Response({"caller_errors": caller_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         caller_instance = caller_serializer.save()
#         incident_data['caller_id'] = caller_instance.pk

#         # Step 2: Save incident
#         incident_serializer = Manual_call_incident_dispatch_Serializer(data=incident_data)
#         if not incident_serializer.is_valid():
#             return Response({"incident_errors": incident_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         incident_instance = incident_serializer.save()

#         base_code = incident_instance.incident_id
#         total_calls = DMS_Incident.objects.filter(alert_code__icontains='CALL-').count()
#         new_call_number = total_calls + 1
#         alert_code = f"CALL-{base_code}"
#         incident_instance.alert_code = alert_code
#         incident_instance.save()

#         # Step 3: Save comments with incident_id = incident_instance.inc_id
#         comments_data['incident_id'] = incident_instance.inc_id  # IMPORTANT: assign inc_id
#         comments_serializer = manual_Comments_Serializer(data=comments_data)
#         if not comments_serializer.is_valid():
#             return Response({"comments_errors": comments_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         comments_instance = comments_serializer.save()

#         incident_instance.comment_id = comments_instance
#         incident_instance.save()

#         # Step 4: Save Weather Alert
#         weather_alert_data = {
#             "alert_code": incident_instance.alert_code,
#             "disaster_id": incident_instance.disaster_type.pk if incident_instance.disaster_type else None,
#             "latitude": incident_instance.latitude,
#             "longitude": incident_instance.longitude,
#             "added_by": incident_instance.inc_added_by,
#             "modified_by": incident_instance.inc_modified_by,
#             "alert_type": incident_instance.alert_type
#         }
#         weather_alert_serializer = WeatherAlertSerializer(data=weather_alert_data)
#         if not weather_alert_serializer.is_valid():
#             return Response({"weather_alert_errors": weather_alert_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         weather_alert_instance = weather_alert_serializer.save()

#         # views.py (inside Manual_Call_Incident_api)
#         dms_notify_data = {
#             "incident_id": incident_instance.inc_id,  # <-- This line adds inc_id to the notify record
#             "disaster_type": incident_instance.disaster_type.pk if incident_instance.disaster_type else None,
#             "alert_type_id": incident_instance.responder_scope,
#             "added_by": incident_instance.inc_added_by
#         }

#         dms_notify_serializer = DMS_NotifySerializer(data=dms_notify_data)
#         if not dms_notify_serializer.is_valid():
#             return Response({"dms_notify_errors": dms_notify_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#         dms_notify_instance = dms_notify_serializer.save()

#         incident_instance.notify_id = dms_notify_instance
#         incident_instance.save()


#         return Response({
#             "message": "Manual call, caller, comment, weather alert, and DMS notify created successfully.",
#             "incident": incident_serializer.data,
#             "caller": caller_serializer.data,
#             "comments": comments_serializer.data,
#             "weather_alert": weather_alert_serializer.data,
#             "dms_notify": dms_notify_serializer.data
#         }, status=status.HTTP_201_CREATED)



import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DMS_Incident
from .serializers import (
    Manual_call_data_Serializer,
    Manual_call_incident_dispatch_Serializer,
    manual_Comments_Serializer,
    WeatherAlertSerializer,
    DMS_NotifySerializer,
)


class Manual_Call_Incident_api(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        incident_fields = [
            'inc_type', 'disaster_type', 'alert_type', 'location', 'summary',
            'responder_scope', 'latitude', 'longitude', 'caller_id',
            'inc_added_by', 'inc_modified_by', 'incident_id', 'inc_id', 'time', 'mode',
            'ward','district','ward_officer','tahsil',
        ]
        caller_fields = ['caller_no', 'caller_name', 'caller_added_by', 'caller_modified_by']
        comments_fields = ['comments', 'comm_added_by', 'comm_modified_by']

        incident_data = {field: data.get(field) for field in incident_fields}
        caller_data = {field: data.get(field) for field in caller_fields}
        comments_data = {field: data.get(field) for field in comments_fields}

       
        caller_serializer = Manual_call_data_Serializer(data=caller_data)
        if not caller_serializer.is_valid():
            return Response({"caller_errors": caller_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        caller_instance = caller_serializer.save()
        incident_data['caller_id'] = caller_instance.pk
        incident_serializer = Manual_call_incident_dispatch_Serializer(data=incident_data)
        if not incident_serializer.is_valid():
            return Response({"incident_errors": incident_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        incident_instance = incident_serializer.save()
        base_code = incident_instance.incident_id
        alert_code = f"CALL-{base_code}"
        incident_instance.alert_code = alert_code
        incident_instance.save()
        comments_data['incident_id'] = incident_instance.inc_id
        comments_serializer = manual_Comments_Serializer(data=comments_data)
        if not comments_serializer.is_valid():
            return Response({"comments_errors": comments_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        comments_instance = comments_serializer.save()
        incident_instance.comment_id = comments_instance
        incident_instance.save()
        
        nn = {"incident_id": incident_instance.incident_id,"alert_comment": comments_instance.comments}
        external_response = requests.post(
                "http://210.212.165.119/Spero_DMS/dms/alert_comments",
                json=nn,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
        print(external_response.json()
 )
 
       
        weather_alert_data = {
            "alert_code": alert_code,
            "disaster_id": incident_instance.disaster_type.pk if incident_instance.disaster_type else None,
            "latitude": incident_instance.latitude,
            "longitude": incident_instance.longitude,
            "added_by": incident_instance.inc_added_by,
            "modified_by": incident_instance.inc_modified_by,
            "alert_type": incident_instance.alert_type
        }
        print("Weather alert data:", weather_alert_data)
        weather_alert_serializer = WeatherAlertSerializer(data=weather_alert_data)
        if not weather_alert_serializer.is_valid():
            print("Weather alert serializer errors:", weather_alert_serializer.errors)
            return Response({"weather_alert_errors": weather_alert_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        weather_alert_instance = weather_alert_serializer.save()
        print("Saved weather alert.")

        # Step 5: Save DMS notify
        dms_notify_data = {
            "incident_id": incident_instance.inc_id,
            "disaster_type": incident_instance.disaster_type.pk if incident_instance.disaster_type else None,
            "alert_type_id": incident_instance.responder_scope,
            "added_by": incident_instance.inc_added_by
        }
        print("DMS notify data:", dms_notify_data)
        dms_notify_serializer = DMS_NotifySerializer(data=dms_notify_data)
        if not dms_notify_serializer.is_valid():
            print("DMS notify serializer errors:", dms_notify_serializer.errors)
            return Response({"dms_notify_errors": dms_notify_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        dms_notify_instance = dms_notify_serializer.save()
        incident_instance.notify_id = dms_notify_instance
        incident_instance.save()
        print("Saved DMS notify.")

        # Step 6: Send to external API
        external_api_payload = {
        "caller_name": caller_instance.caller_name,
        "caller_no": caller_instance.caller_no,
        "disaster_name": str(incident_instance.disaster_type.disaster_name) if incident_instance.disaster_type else "",
        "location": incident_instance.location,
        "summary": str(incident_instance.summary.summary),
        # "inc_type": "NON_MCI" if incident_instance.inc_type == 1 else "NON_EME_CALL" if incident_instance.inc_type == 2 else "",
        "inc_type": incident_instance.disaster_type.disaster_id if incident_instance.disaster_type else None,
        "incident_id": str(incident_instance.incident_id),
        "latitude": str(incident_instance.latitude),
        "longitude": str(incident_instance.longitude),
        "dms_lat": str(incident_instance.latitude),
        "dms_lng": str(incident_instance.longitude),
        "alert_type": ("High" if incident_instance.alert_type == 1 else"Medium" if incident_instance.alert_type == 2 else"Low" if incident_instance.alert_type == 3 else"Very Low" if incident_instance.alert_type == 4 else""
)
    }
        print("ssssssssssssssssssssssssss",external_api_payload)
        print("Sending to external API:", external_api_payload)

        try:
            external_response = requests.post(
                "http://210.212.165.119/Spero_DMS/dms/alert_details",
                json=external_api_payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            print("External API status:", external_response.status_code)
            print("External API raw response:", external_response.text)
            if external_response.status_code == 200:
                external_api_result = external_response.json()
            else:
                external_api_result = {
                    "error": f"Status {external_response.status_code}",
                    "response": external_response.text
                }
        except Exception as e:
            print("Exception during external API call:", str(e))
            external_api_result = {"error": str(e)}

        # Final response
        return Response({
            "message": "Manual call, caller, comment, weather alert, DMS notify created successfully and external API called.",
            "incident": incident_serializer.data,
            "caller": caller_serializer.data,
            "comments": comments_serializer.data,
            "weather_alert": weather_alert_serializer.data,
            "dms_notify": dms_notify_serializer.data,
            "external_api_response": external_api_result
        }, status=status.HTTP_201_CREATED)






class Responder_Scope_Get_api(APIView):
    def get(self, request, disaster_id):
        sop_responses = DMS_SOP.objects.filter(disaster_id=disaster_id)
        sop_serializer = Sop_Response_Procedure_Serializer(sop_responses, many=True)

        disaster_responders = DMS_Disaster_Responder.objects.filter(dr_is_deleted=False, dis_id=disaster_id)

        responder_scope_data = []

        for dr in disaster_responders:
            res_ids = dr.res_id if isinstance(dr.res_id, list) else []
            responders = DMS_Responder.objects.filter(responder_id__in=res_ids)
            for responder in responders:
                responder_scope_data.append({
                    "res_id": responder.responder_id,
                    "responder_name": responder.responder_name
                })

        return Response({
            "sop_responses": sop_serializer.data,
            "responder_scope": responder_scope_data
        }, status=status.HTTP_200_OK)

        
class DMS_Summary_Get_API(APIView):
    def get(self,request,summary_type):
        snippet = DMS_Summary.objects.filter(summary_type=summary_type)
        serializers = DMS_Summary_Serializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
# class DMS_responder_post_api(APIView):
#     def post(self,request):
#         serializers=Responder_serializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data,status=status.HTTP_201_CREATED)
#         return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


# class DMS_responder_put_api(APIView):
#     def get(self, request, responder_id):
#         snippet = DMS_Responder.objects.filter(responder_id=responder_id,responder_is_deleted=False)
#         serializers = Responder_Serializer(snippet, many=True)
#         return Response(serializers.data)

#     def put(self, request, responder_id):
#         try:
#             instance = DMS_Responder.objects.get(responder_id=responder_id)
#         except DMS_Responder.DoesNotExist:
#             return Response({"error": "Responder not found."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = Responder_serializer(instance, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# class DMS_responder_delete_api(APIView):
#     def get(self, request, responder_id):
#         try:
#             instance = DMS_Responder.objects.get(responder_id=responder_id, responder_is_deleted=False)
#         except DMS_SOP.DoesNotExist:
#             return Response({"error": "Responder not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = Responder_Serializer(instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def delete(self, request, sop_id):
#         try:
#             instance = DMS_Responder.objects.get(responder_id=responder_id, responder_is_deleted=False)
#         except DMS_Responder.DoesNotExist:
#             return Response({"error": "Responder not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)

#         instance.responder_is_deleted = True
#         instance.save()
#         return Response({"message": "Responder soft deleted successfully."}, status=status.HTTP_200_OK)

class GetResponderList_api(APIView):
    def get(self, request):
        responders = DMS_Responder.objects.filter(responder_is_deleted=False)
        serializer = Responder_Serializer(responders, many=True)
        return Response(serializer.data)


class disaster_responder_Post_api(APIView):
    def post(self, request):
        dis_id = request.data.get('dis_id')

        if dis_id is None:
            return Response({"error": "dis_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        existing = DMS_Disaster_Responder.objects.filter(dis_id=dis_id, dr_is_deleted=False).first()

        if existing:
            return Response(
                {"error": "This dis_id already exists."},
                status=status.HTTP_409_CONFLICT
            )

        serializers = Responder_Scope_post_Serializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class Disaster_Responder_put(APIView):
    def get(self, request, pk_id):
        snippet = DMS_Disaster_Responder.objects.filter(pk_id=pk_id,dr_is_deleted=False)
        serializers = DisasterResponderSerializer(snippet, many=True)
        return Response(serializers.data)
    def put(self,request,pk_id):
        try:
            instance =DMS_Disaster_Responder.objects.get(pk_id=pk_id)
        except DMS_Disaster_Responder.DoesNotExist:
            return Response({"error": "record not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DisasterResponderSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Disaster_responder_delete_api(APIView):
    def get(self, request, pk_id):
        try:
            instance = DMS_Disaster_Responder.objects.get(pk_id=pk_id, dr_is_deleted=False)
        except DMS_Disaster_Responder.DoesNotExist:
            return Response({"error": "record not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)
        serializer = Responder_Serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk_id):
        try:
            instance = DMS_Disaster_Responder.objects.get(pk_id=pk_id, dr_is_deleted=False)
        except DMS_Disaster_Responder.DoesNotExist:
            return Response({"error": "record not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)

        instance.dr_is_deleted = True
        instance.save()
        return Response({"message": "Record soft deleted successfully."}, status=status.HTTP_200_OK)


# class disaster_responder_Post_api(APIView):
#     def post(self,request):
#         serializers=DisasterResponderPostSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data,status=status.HTTP_201_CREATED)
#         return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class DMS_Disaster_Responder_GET_API(APIView):
    def get(self, request):
        pk_id = request.query_params.get('pk_id')
        queryset = DMS_Disaster_Responder.objects.filter(dr_is_deleted=False)

        if pk_id is not None:
            queryset = queryset.filter(pk_id=pk_id)

        response_data = []

        for obj in queryset:
            serialized_data = DisasterResponderSerializer(obj).data

            res_ids = obj.res_id if isinstance(obj.res_id, list) else []

            responder_details = list(
                DMS_Responder.objects
                .filter(responder_id__in=res_ids)
                .values('responder_id', 'responder_name')
            )

            serialized_data['res_id'] = responder_details

            response_data.append(serialized_data)

        return Response(response_data)


# class closure_Post_api(APIView):
#     def post(self, request):
        
#         inccc = request.data.get('incident_id')
#         print(inccc,'innnnnnnnn')
#         nnnnnn = DMS_Incident.objects.get(inc_id=inccc)
#         nnnnnn.clouser_status = True
#         nnnnnn.save()
#         serializer = ClosureSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class closure_Post_api(APIView):
    def post(self, request):
        try:
            inccc = request.data.get('incident_id')
            dpt = request.data.get('responder')

            inc_dtl = DMS_Incident.objects.get(incident_id=inccc)
            dpt_dtl = DMS_Responder.objects.get(responder_name=dpt)
            inc_dpts = DMS_Notify.objects.filter(incident_id=inc_dtl, not_is_deleted=False)
            inc_dpts_ids = sorted([int(j) for i in inc_dpts for j in i.alert_type_id])
            get_closure_dtl = DMS_incident_closure.objects.filter(
                incident_id=inc_dtl, responder=dpt_dtl, closure_is_deleted=False
            )
            all_clsr_dtls = DMS_incident_closure.objects.filter(incident_id=inc_dtl, closure_is_deleted=False)
            if get_closure_dtl.exists():
                inc_dtl.clouser_status = True
                inc_dtl.save()
                cl_dpts = sorted(all_clsr_dtls.values_list('responder', flat=True))
                unmatched_from_inc = set(inc_dpts_ids) - set(cl_dpts)
                get_unmatch_dpt_clsr_ntdn = DMS_Responder.objects.filter(responder_id__in=unmatched_from_inc)
                dpts_unm_nms = get_unmatch_dpt_clsr_ntdn.values_list('responder_name', flat=True)
                return Response({"msg":f"Closure already done for incident {inc_dtl.incident_id} of that department/Responder {dpt_dtl.responder_name}",
                                 "Closure_Pending_Responders": dpts_unm_nms},status=status.HTTP_200_OK)
            else:
                cls_dtl_add = DMS_incident_closure.objects.create(
                    incident_id=inc_dtl,
                    responder=dpt_dtl,
                    vehicle_no=request.data.get('vehicle_no'),
                    closure_acknowledge=request.data.get('closure_acknowledge'),
                    closure_start_base_location=request.data.get('closure_start_base_location'),
                    closure_at_scene=request.data.get('closure_at_scene'),
                    closure_from_scene=request.data.get('closure_from_scene'),
                    closure_back_to_base=request.data.get('closure_back_to_base'),
                    # incident_responder_by=request.data.get('incident_responder_by'),
                    closure_responder_name=request.data.get('closure_responder_name'),
                    closure_is_deleted=False,
                    closure_added_by=request.data.get('closure_added_by'),
                    closure_modified_by=request.data.get('closure_modified_by'),
                    closure_modified_date=request.data.get('closure_modified_date'),
                    closure_remark=request.data.get('closure_remark')
                )
                
                cl_dpts = sorted(all_clsr_dtls.values_list('responder', flat=True))
                if cl_dpts == inc_dpts_ids:
                    inc_dtl.clouser_status = True
                    inc_dtl.save()
                    return Response("Closure done for all departments.", status=status.HTTP_201_CREATED)
                else:
                    unmatched_from_inc = set(inc_dpts_ids) - set(cl_dpts)
                    get_unmatch_dpt_clsr_ntdn = DMS_Responder.objects.filter(responder_id__in=unmatched_from_inc)
                    dpts_unm_nms = get_unmatch_dpt_clsr_ntdn.values_list('responder_name', flat=True)
                    if len(dpts_unm_nms) == 0:
                        return Response({
                            "msg": f"Closure for {dpt_dtl.responder_name} is done",
                            "Departments": "All Department Closure Done"
                        }, status=status.HTTP_201_CREATED)
                    else: 
                        return Response({
                        "msg": f"Closure for {dpt_dtl.responder_name} is done, but remaining departments pending: {list(dpts_unm_nms)}",
                        "Departments": list(dpts_unm_nms)
                    }, status=status.HTTP_201_CREATED)

        except DMS_Incident.DoesNotExist:
            return Response({"error": "Incident not found."}, status=status.HTTP_404_NOT_FOUND)
        except DMS_Department.DoesNotExist:
            return Response({"error": "Department not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class closure_Post_api2(APIView):
    def post(self, request):
        closure_inc_id = request.data.get('closure_inc_id')
        print(closure_inc_id, 'closure_inc_id')

        try:
            incident_obj = DMS_Incident.objects.get(incident_id=closure_inc_id)
            incident_obj.clouser_status = True
            incident_obj.save()
        except DMS_Incident.DoesNotExist:
            return Response({"error": "Incident not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClosureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class comment_idwise_get_api(APIView):
    def get(self, request, incident_id):
        comments_qs = DMS_Comments.objects.filter(incident_id=incident_id, comm_is_deleted=False)
        comment_texts = comments_qs.values_list('comments', flat=True)
        data = {
            "incident_id": incident_id,
            "comments": list(comment_texts)
        }
        return Response(data, status=status.HTTP_200_OK)

class DMS_comment_Get_API(APIView):
    def get(self,request):
        snippet = DMS_Comments.objects.all()
        serializers = CommentSerializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

# class dispatch_sop_Get_API(APIView):
#     def get(self,request):
#         snippet = DMS_Incident.objects.all().order_by('-inc_added_date')
#         serializers = dispatchsopserializer(snippet,many=True)
#         print(serializers.data)
#         return Response(serializers.data,status=status.HTTP_200_OK)


class dispatch_sop_Get_API(APIView):
    def get(self,request):
        snippet = DMS_Incident.objects.filter(clouser_status=False).order_by('-inc_added_date')
        serializers = dispatchsopserializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class dispatch_sop_Idwise_Get_API(APIView):
    def get(self,request, inc_id):
        snippet = DMS_Incident.objects.filter(inc_is_deleted=False,inc_id=inc_id)
        serializers = dispatchsopserializer(snippet,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    








from django.shortcuts import get_object_or_404
# class CommentPostView(APIView):
#     def post(self, request, incident_id):
#         # Use correct PK field: inc_id
#         incident_instance = get_object_or_404(DMS_Incident, inc_id=incident_id)

#         serializer = Comment_Post_Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(incident_id=incident_instance)
            
#             aaa=DMS_Incident.objects.filter(inc_id=incident_id)
            
#             nn = {"incident_id": aaa.incident_id,"alert_comment": serializer.data.get('comments')}
#             external_response = requests.post(
#                     "http://210.212.165.119/Spero_DMS/dms/alert_details",
#                     json=nn,
#                     headers={"Content-Type": "application/json"},
#                     timeout=10
#                 )
#             print(external_response.json()
#  )
            
            
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

class CommentPostView(APIView):
    def post(self, request, incident_id):
        incident_instance = get_object_or_404(DMS_Incident, inc_id=incident_id)

        serializer = Comment_Post_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(incident_id=incident_instance)
            
            aaa = DMS_Incident.objects.get(inc_id=incident_id)
            
            nn = {
                "incident_id": aaa.incident_id,
                "alert_comment": serializer.data.get('comments')
            }

            try:
                external_response = requests.post(
                    "http://210.212.165.119/Spero_DMS/dms/alert_details",
                    json=nn,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                external_data = external_response.json()
            except requests.exceptions.RequestException as e:
                external_data = {"error": str(e)}

            return Response({
                "local_data": serializer.data,
                "external_api_response": external_data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class incident_get_Api(APIView):
    def get(self, request, inc_id):
        # Directly get the incident object
        incident_qs = DMS_Incident.objects.filter(inc_id=inc_id).order_by('inc_added_date')
        incident_serializer = incident_get_serializer(incident_qs, many=True)
        incident_data = incident_serializer.data

        # Get responder IDs directly from the ArrayField
        responder_ids = []
        if incident_data:
            raw_ids = incident_data[0].get('responder_scope', [])
            responder_ids = [int(rid) for rid in raw_ids if str(rid).isdigit()]

        # Get responder details
        responders = DMS_Responder.objects.filter(responder_id__in=responder_ids).values('responder_id', 'responder_name')
        responder_details = list(responders)

        # Get related comments
        comments_qs = DMS_Comments.objects.filter(incident_id=inc_id, comm_is_deleted=False)
        comment_texts = comments_qs.values('comm_id', 'comments','comm_added_by','comm_added_date')

        # Final response
        data = {
            "incident_details": incident_data,
            "inc_id": inc_id,
            "comments": list(comment_texts),
            "responders scope": responder_details
        }
        return Response(data, status=status.HTTP_200_OK)



#-----------------------------cancel Dispatch API ----------------------
class UpdateTriggerStatusAPIView(APIView):
    def post(self, request):
        pk_id = request.data.get('id')

        if not pk_id:
            return Response({'status': False, 'message': 'ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = Weather_alerts.objects.get(pk_id=pk_id)
        except Weather_alerts.DoesNotExist:
            return Response({'status': False, 'message': 'Record not found.'}, status=status.HTTP_404_NOT_FOUND)

        if record.triger_status == 2:
            record.triger_status = 1
            record.save(update_fields=['triger_status'])
            return Response({'status': True, 'message': f'Record with ID {pk_id} updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'message': f'Record with ID {pk_id} already has triger_status = {record.triger_status}.'
            }, status=status.HTTP_200_OK)
            


        
class incident_wise_responder_list(APIView):
    def get(self, request,inc_id):
        res_lst = list(set([]))
        nid = DMS_Notify.objects.filter(incident_id=inc_id)
        for i in nid:
            for j in list(set(i.alert_type_id)):
                res_lst.append(j)
        kk=[]
        vv = DMS_incident_closure.objects.filter(incident_id=inc_id, closure_is_deleted=False)
        rs_ids = set(vv.values_list('responder', flat=True))
        ll = sorted(set(int(x) for x in res_lst if int(x) not in rs_ids))
        for m in ll:
            mm=DMS_Responder.objects.get(responder_id=int(m))
            dt={
                'responder_id':mm.responder_id,
                'responder_name':mm.responder_name
                 }
            kk.append(dt)
        return Response(kk)




class Ward_get_API(APIView):
    def get(self,request,tah_id):
        ward = DMS_Ward.objects.filter(tah_id=tah_id).order_by('pk_id')
        serializer = Ward_get_Serializer(ward,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class Ward_Officer_get_API(APIView):
    def get(self,request,ward_id):
        ward = DMS_Employee.objects.filter(ward_id=ward_id,grp_id_id__grp_name='Ward Officer')
        serializer = Ward_officer_get_Serializer(ward,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    