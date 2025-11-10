from enum import Enum


class RoleEnum(str, Enum):
    MAIN_DOCTOR = "main_doctor"
    ADMIN = "admin"
    EMPLOYEE_HOSPITAL = "employee_hospital"
