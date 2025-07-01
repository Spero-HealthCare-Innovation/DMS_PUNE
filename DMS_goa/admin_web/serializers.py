from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from captcha.models import CaptchaStore
from .models import *
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
from admin_web.models import DMS_Employee

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Optional: add Django's password validation
        password_validation.validate_password(value)
        return value
    
class ForgotPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Optional: add Django's password validation
        password_validation.validate_password(value)
        return value
    
class PasswordResetRequestSerializer(serializers.Serializer):
    emp_email = serializers.EmailField()

    def validate_email(self, value):
        if not DMS_Employee.objects.filter(emp_email=value).exists():
            raise serializers.ValidationError("No user with this email.")
        return value
    


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uid']).decode()
            user = DMS_Employee.objects.get(pk=uid)
        except (DMS_Employee.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError({"uid": "Invalid UID"})

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError({"token": "Invalid or expired token"})

        validate_password(attrs['new_password'])

        attrs['user'] = user
        return attrs
    

class DMS_department_serializer(serializers.ModelSerializer):
    class Meta:
        model=DMS_Department
        fields='__all__'

class DMS_Group_serializer(serializers.ModelSerializer):
    dep_name = serializers.CharField(source='dep_id.dep_name', read_only=True)
    class Meta:
        model=DMS_Group
        fields='__all__'

class DMS_Employee_serializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    # grp_id = serializers.PrimaryKeyRelatedField(queryset=DMS_Group.objects.all(),many=False)
    
    class Meta:
        model  = DMS_Employee
        fields = ['emp_id', 'emp_username', 'grp_id', 'emp_name', 'emp_email', 'emp_contact_no', 'emp_dob', 'emp_doj', 'emp_is_login', 'state_id', 'dist_id', 'tahsil_id', 'city_id', 'emp_is_deleted', 'emp_added_by', 'emp_modified_by', 'password','password2','ward_id' ]

        extra_kwargs = {
            'password':{'write_only':True}
        }
        
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match')

        return data
    
    def create(self, validated_data):
        group_data = validated_data.pop('grp_id')
        validated_data['grp_id'] = group_data

        # Hash the password before creating the user
        password = validated_data.pop('password')
        user = DMS_Employee.objects.create_user(**validated_data)
        user.set_password(password)  # hashes and sets it correctly
        user.save()
        return user
    
    

class DMS_Employee_GET_serializer(serializers.ModelSerializer):
    
    dis_name = serializers.CharField(source='dist_id.dis_name', read_only=True)
    tah_name = serializers.CharField(source='tahsil_id.tah_name', read_only=True)
    cit_name = serializers.CharField(source='city_id.cit_name', read_only=True)
    grp_name = serializers.CharField(source='grp_id.grp_name', read_only=True)
    state_name = serializers.CharField(source='state_id.state_name', read_only=True)
    ward_name = serializers.CharField(source='ward_id.ward_name', read_only=True)
    

    class Meta:
        model = DMS_Employee
        fields = [
            'emp_id', 'emp_username', 'grp_id', 'emp_name', 'emp_email',
            'emp_contact_no', 'emp_dob', 'emp_doj', 'emp_is_login',
            'state_id', 'state_name', 'dist_id','dis_name','tahsil_id','tah_name','city_id','cit_name','grp_name',
            'emp_is_deleted', 'emp_added_by', 'emp_modified_by', 'password','ward_id','ward_name'
        ]
        
    
class DMS_District_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_District
        fields = '__all__'
    
class DMS_Tahsil_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Tahsil
        fields = '__all__'

class DMS_City_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_City
        fields = '__all__'

class DMS_State_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_State
        fields = '__all__'
        
class DMS_Group_Serializer(serializers.ModelSerializer):
    dep_name = serializers.CharField(source='dep_id.dep_name', read_only=True)
    class Meta:
        model = DMS_Group
        fields = '__all__'
        
class DMS_Department_Serializer(serializers.ModelSerializer):
    dst_name = serializers.CharField(source='dis_id.dis_name', read_only=True)
    state_name = serializers.CharField(source='state_id.state_name', read_only=True)
    tah_name = serializers.CharField(source='tah_id.tah_name', read_only=True)
    city_name = serializers.CharField(source='cit_id.cit_name', read_only=True)
    class Meta:
        model = DMS_Department
        fields = '__all__'
        
class DMS_Disaster_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Disaster_Type
        fields = '__all__'
              

# ============= Permission Module Serializer ============================

class Mmoduleserializer(serializers.ModelSerializer):
    #  grp_name = serializers.CharField(source='mod_group_id.grp_name', allow_null=True)
    #  department_id = serializers.CharField(source='mod_group_id.dep_id.dep_id', allow_null=True)
    #  department_name = serializers.CharField(source='mod_group_id.dep_id.dep_name', allow_null=True)

     class Meta:
          model = DMS_Module
          fields = ['mod_id', 'mod_name', 'mod_group_id', 'grp_name']


class permission_sub_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_SubModule
        fields = '__all__'




class CaptchaTokenObtainPairSerializer(TokenObtainPairSerializer):
    captcha_key = serializers.CharField(write_only=True)
    captcha_value = serializers.CharField(write_only=True)

    def validate(self, attrs):
        key = attrs.pop('captcha_key', '')
        value = attrs.pop('captcha_value', '')

        # Validate CAPTCHA
        try:
            captcha = CaptchaStore.objects.get(hashkey=key)
            if captcha.response != value.lower():
                raise serializers.ValidationError("Invalid CAPTCHA.")
            captcha.delete()  # optional: one-time use
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError("Invalid CAPTCHA key.")

        return super().validate(attrs)
        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['group'] = user.grp_id  # Add role to JWT payload
        return token
    

class UserLoginSerializer(serializers.ModelSerializer):
    emp_username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        model = DMS_Employee
        fields = ['emp_username', 'password']


class ChangePasswordGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Employee
        fields = [ 'emp_id','emp_username','password']

class ChangePasswordputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Employee
        fields = ['password']

class SopSerializer(serializers.ModelSerializer):
    disaster_name=serializers.CharField(source='disaster_id.disaster_name', read_only=True)
    class Meta:
        model = DMS_SOP
        # fields = '__all__'
        fields = ['sop_id','sop_description','disaster_id','sop_added_by','sop_modified_by','disaster_name']
        
class Sop_Put_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_SOP
        fields = ['sop_description','disaster_id']

class WeatherAlertSerializer(serializers.ModelSerializer):
    disaster_name = serializers.SerializerMethodField()

    class Meta:
        model = Weather_alerts
        fields = '__all__'

    def get_disaster_name(self, obj):
        if obj.disaster_id:
            return obj.disaster_id.disaster_name  # assuming `disaster_name` is a field in DMS_Disaster_Type
        return None

# class Incident_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = DMS_Incident
#         fields = '__all__' 

class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Notify
        fields = ['alert_type_id','disaster_type','alert_code']

        
class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Comments
        exclude = ['alert_id','comm_modified_by','comm_modified_date']

class Incident_Serializer(serializers.ModelSerializer):
    responder_scope = serializers.ListField(child=serializers.CharField(), write_only=True)
    comments = serializers.CharField(write_only=True)
    comm_added_by = serializers.CharField(write_only=True)

    class Meta:
        model = DMS_Incident
        fields = '__all__'
        extra_fields = ['latitude','longitude','responder_scope', 'comments', 'comm_added_by']

    def create(self, validated_data):
        responder_scope = validated_data.pop('responder_scope', [])
        comments_text = validated_data.pop('comments')
        comm_added_by = validated_data.pop('comm_added_by')

        incident = DMS_Incident.objects.create(
            responder_scope=responder_scope,
            **validated_data
        )

        notify = DMS_Notify.objects.create(
            alert_type_id=responder_scope,
            disaster_type=incident.disaster_type,
            not_added_by=incident.inc_added_by,
            incident_id=incident  
        )

        incident.notify_id = notify
        incident.save(update_fields=['notify_id'])


        comment = DMS_Comments.objects.create(
            alert_id=incident.alert_id,
            incident_id=incident,
            comments=comments_text,
            comm_added_by=comm_added_by
        )

        incident.comment_id = comment
        incident.save(update_fields=['comment_id'])

        return incident


        
class Comments_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Comments
        fields = '__all__' 
        
class Sop_Response_Procedure_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_SOP
        fields = ['sop_id','sop_description']

# class Responder_Scope_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = DMS_Notify
#         fields = ['alert_type_id']





        
class Alert_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Alert_Type
        fields = ['alert_name']
        

class Manual_call_incident_dispatch_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Incident
        fields = ['inc_type','disaster_type','alert_type','location','summary','responder_scope','latitude','longitude','caller_id','inc_added_by','inc_modified_by','time','mode','ward','district','ward_officer','tahsil','ward','district','ward_officer','tahsil']   

class Manual_call_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Caller
        fields = ['caller_no','caller_name','caller_added_by','caller_modified_by']
        
class manual_Comments_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Comments
        fields = ['incident_id','comments','comm_added_by','comm_modified_by'] 
        
class Responder_Scope_Serializer(serializers.ModelSerializer):
    responder_names = serializers.SerializerMethodField()

    class Meta:
        model = DMS_Disaster_Responder
        fields = ['pk_id', 'res_id', 'responder_names']

    def get_responder_names(self, obj):
        if isinstance(obj.res_id, list):
            responder_ids = obj.res_id
        else:
            try:
                import json
                responder_ids = json.loads(obj.res_id)
            except:
                responder_ids = []

        responders = DMS_Responder.objects.filter(responder_id__in=responder_ids)
        return [r.responder_name for r in responders]

        
        
class DMS_NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Notify
        fields = '__all__'
        
class DMS_Summary_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Summary
        fields = ['sum_id','summary']


class Responder_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Responder
        fields = ['responder_id', 'responder_name']

class DisasterResponderSerializer(serializers.ModelSerializer):
    disaster_name=serializers.CharField(source='dis_id.disaster_name', read_only=True)
    class Meta:
         model = DMS_Disaster_Responder
         fields = '__all__'

class DisasterResponderPostSerializer(serializers.ModelSerializer):
    class Meta:
         model = DMS_Disaster_Responder
         fields = ['dis_id','res_id']

class ClosureSerializer2(serializers.ModelSerializer):
    closure_inc_id = serializers.CharField()  

    class Meta:
        model = DMS_incident_closure
        fields = '__all__'

    def create(self, validated_data):
        closure_inc_id = validated_data.get('closure_inc_id')

        try:
            incident_obj = DMS_Incident.objects.get(incident_id=closure_inc_id)
            validated_data['incident_id'] = incident_obj
        except DMS_Incident.DoesNotExist:
            raise serializers.ValidationError({'closure_inc_id': 'Invalid incident ID'})

        return super().create(validated_data)
    

class ClosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_incident_closure
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Comments
        fields = ['incident_id','comments','comm_added_by']


class Comment_Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Comments
        fields = ['incident_id','comments','comm_added_by','comm_modified_by']

class dispatchsopserializer(serializers.ModelSerializer):
    disaster_name=serializers.CharField(source='disaster_type.disaster_name', read_only=True)
    alert_id = serializers.CharField(source='alert_id.disaster_name', read_only=True)
    class Meta:
        model = DMS_Incident
        fields = ['inc_id','incident_id','alert_id','disaster_type','inc_added_by','inc_added_date','disaster_name','inc_type','mode','alert_type']
        


class incident_get_serializer(serializers.ModelSerializer):
    caller_name=serializers.CharField(source='caller_id.caller_name', read_only=True)
    caller_no=serializers.CharField(source='caller_id.caller_no', read_only=True)
    summary_name = serializers.CharField(source='summary.summary', read_only=True)
    disaster_name=serializers.CharField(source='disaster_type.disaster_name', read_only=True)
    comment_added_by = serializers.CharField(source='comment_id.comm_added_by',read_only=True)
    ward_name = serializers.CharField(source='ward.ward_name',read_only=True)
    district_name = serializers.CharField(source='district.dis_name',read_only=True)
    tahsil_name = serializers.CharField(source='tahsil.tah_name',read_only=True)
    ward_officer_name = serializers.SerializerMethodField()
    
    
    class Meta:
        model = DMS_Incident
        fields=['incident_id','disaster_type','inc_type','responder_scope','caller_id','caller_name','caller_no','location','summary','summary_name','disaster_name','alert_type','mode','latitude','longitude','inc_datetime','location','comment_added_by','ward','district','ward_officer','tahsil','ward_name','district_name','tahsil_name','ward_officer_name']

    
    def get_ward_officer_name(self, obj):
        try:
            officer_ids = obj.ward_officer if isinstance(obj.ward_officer, list) else []
            officers = DMS_Employee.objects.filter(emp_id__in=officer_ids)
            return [{"emp_id": officer.emp_id, "ward_officer_name": officer.emp_name} for officer in officers]
        except Exception:
            return []
        
        
        

class Responder_Scope_post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Disaster_Responder
        fields = ['res_id','dis_id','dr_added_by','dr_modified_by']
        

class Ward_get_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Ward
        # fields = '__all__'
        fields = ['pk_id','ward_name']


class Ward_officer_get_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DMS_Employee
        # fields = '__all__'
        fields = ['emp_id','emp_name']