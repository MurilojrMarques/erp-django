from rest_framework.exceptions import AuthenticationFailed, APIException
from django.db import transaction # Importante para segurança de dados
from .models import Users
from companies.models import Company, Employee, Department
from django.contrib.auth.hashers import check_password

class Authentication:
    
    @staticmethod
    def sign_in(email, password) -> Users:
        auth_error = AuthenticationFailed("Email e/ou senha inválidos")
        user = Users.objects.filter(email=email).first()
        
        if not user or not check_password(password, user.password):
            raise auth_error
        return user
    
    @staticmethod
    def sign_up(name, email, password, is_admin=False, company_id=None) -> Users:
        if not name: raise APIException("Nome é obrigatório")
        if not email: raise APIException("Email é obrigatório")
        if not password: raise APIException("Senha é obrigatória")

        is_admin = bool(is_admin)
        company = None
        if not is_admin:
            if not company_id:
                raise APIException("O ID da empresa é obrigatório para funcionários")
            
            company = Company.objects.filter(id=company_id).first()
            if not company:
                raise APIException("Empresa não encontrada")
             
        if Users.objects.filter(email=email).exists():
            raise APIException("Email já cadastrado")

        try:
            with transaction.atomic():
                user = Users(
                    name=name, 
                    email=email, 
                    username=email, 
                    is_admin=is_admin,
                    company=company
                )
                user.set_password(password)
                user.save()

                if not is_admin:
                    dept, _ = Department.objects.get_or_create(
                        name="Geral", 
                        company=company
                    )
                    
                    Employee.objects.create(
                        user=user,
                        company=company,
                        department=dept
                    )
                
                return user
        except Exception as e:
            raise APIException(f"Erro ao criar conta: {str(e)}")