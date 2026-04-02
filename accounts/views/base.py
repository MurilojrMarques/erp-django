from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from companies.models import Company, Employee
from accounts.models import UserGroup, Users

class Base(APIView):
    def get_company_user(self, user_id):
        user = Users.objects.filter(id=user_id).first()
        if not user:
            raise APIException("Usuário não encontrado.")
        
        company = {
            "is_admin": user.is_admin,
            "permissons": []
        }

        if user.is_admin:
            return company
        
        employee = Employee.objects.filter(user_id=user_id).first()

        if not employee:
            raise APIException("Esse usuário não pertence a nenhuma empresa.")
        
        user_groups = UserGroup.objects.filter(user_id=user_id).select_related('group').prefetch_related('group__permissions').all()

        permissions_list = []

        for ug in user_groups:
            group_permissions = ug.group.permissions.all()
            for perm in group_permissions:
                if perm.codename not in permissions_list:
                    permissions_list.append(perm.codename)

        company["permissions"] = permissions_list
        return company