from django.db import models
import django.utils.timezone as timezone


# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)

    class Meta:
        db_table = 'bt_user'
        verbose_name = verbose_name_plural = '用户信息表'

    def __str__(self):
        return self.username


class UserToken(models.Model):
    username = models.OneToOneField(to='User',on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=60)

    class Meta:
        db_table =  'bt_user_token'
        verbose_name = verbose_name_plural = '用户token表'


class GlobalData(models.Model):
    """
    全局变量参数
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128,verbose_name="全部变量名称",unique=True)
    description = models.CharField(max_length=512,verbose_name="全局变量说明",null=True,blank=True)
    params = models.CharField(max_length=512,verbose_name="变量参数值")

    class Meta:
        db_table = 'bt_global'
        verbose_name = verbose_name_plural = "全局变量表"

    def __str__(self):
        return self.name


class Project(models.Model):
    """项目表"""
    project_type = (
        ('web','web'),
        ('App','App')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,verbose_name='项目名称',unique=True)
    version = models.CharField(max_length=50,verbose_name='项目版本')
    type = models.CharField(max_length=50,verbose_name='项目类型',choices=project_type)
    description = models.CharField(max_length=1024,blank=True,null=True,verbose_name='描述')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    user_id = models.IntegerField(verbose_name='创建者id',unique=False,blank=False,null =True)
    # null =True 数据库可以为空
    # blank = True只是可以不传数据
    class Meta:
        db_table = 'bt_project'
        verbose_name = verbose_name_plural = "项目表"

    def __str__(self):
        return self.name


class CaseGroup(models.Model):
    """用例分组表"""

    id = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=200,verbose_name='组名称',unique=True)
    description = models.CharField(max_length=1024,blank=True,null=True,verbose_name='描述')
    projectId = models.IntegerField(verbose_name='项目id')
    createTime = models.DateTimeField(verbose_name="保存日期",default=timezone.now)
    updateTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bt_case_group'
        verbose_name = verbose_name_plural = '用例分组表'

    def __str__(self):
        return self.groupName


class Case(models.Model):
    """case 表"""
    id = models.AutoField(primary_key=True)
    caseName = models.CharField(max_length=200,verbose_name='用例名称',unique=True)
    datails = models.CharField(max_length=1024,blank=True,null=True,verbose_name='描述')
    caseGroupId = models.IntegerField(verbose_name='用例组id')
    report = models.CharField(max_length=1024,verbose_name='用例结果')

    class Meta:
        db_table = 'bt_case'
        verbose_name = verbose_name_plural = '用例表'

    def __str__(self):
        return self.caseName


class CaseProcedure(models.Model):
    """用例执行步骤表"""

    judge_word_key_word_type = (
        (">","GreaterThan"),
        ("<","LessThan"),
        ("<=","EqualOrLessThan"),
        (">=","EqualAndGreaterThan"),
        ("==","Equal"),
        ("in","Contain"),
        ("not in","NotContain"),
    )
    id = models.AutoField(primary_key=True)
    caseId = models.IntegerField(verbose_name='用例id')
    datails = models.CharField(max_length=256,verbose_name='操作步骤描述',blank=True,null=True)
    KeyWord = models.CharField(max_length=256,verbose_name='关键字')
    element = models.CharField(max_length=256,verbose_name='元素及定位方式')
    returnValue = models.CharField(max_length=256,verbose_name='元素操作的返回值',blank=True,null=True)
    step = models.IntegerField(verbose_name='步骤顺序',blank=False,null=False)
    link_step_id = models.CharField(max_length=256,verbose_name='关联上一步',blank=True,null=True)   # model id->1
    judge_key_word = models.CharField(max_length=256,verbose_name="判断类型",choices= judge_word_key_word_type,blank=True,null=True)
    judge_value = models.CharField(max_length=256,verbose_name="判断比较的值",blank=True,null=True)
    judge_step_set = models.CharField(max_length=256,verbose_name="条件语句成立执行语句",blank=True,null=True)
    for_step_set = models.CharField(max_length=256,verbose_name="for循环执行语句",blank=True,null=True)
    RunTime = models.CharField(max_length=256,verbose_name='执行时间',blank=True,null=True)

    class Meta:
        db_table = 'bt_case_procedure'
        verbose_name = verbose_name_plural = '用例模板表'

    def __str__(self):
        return self.id


class CaseParameter(models.Model):
    """
    用例参数表
    """
    id = models.AutoField(primary_key=True)
    caseId = models.IntegerField(verbose_name='用例id')
    ProceduceId = models.IntegerField(verbose_name="用例步骤id")
    paramsValues = models.CharField(max_length=1024,verbose_name="步骤参数")

    class Meta:
        db_table = "bt_case_params"
        verbose_name = verbose_name_plural = "用例参数"

    def __str__(self):
        return self.id


class CheckCase(models.Model):
    """用例检查点表"""
    id = models.AutoField(primary_key=True)
    CaseId = models.IntegerField(verbose_name='用例id')
    seq = models.IntegerField(verbose_name='步骤顺序')
    datails = models.CharField(max_length=1024, verbose_name='操作步骤描述')
    KeyWord = models.CharField(max_length=1024, verbose_name='关键字')
    type = models.CharField(max_length=1024, verbose_name='定位方式')
    ele = models.CharField(max_length=1024, verbose_name='操作元素')
    value = models.CharField(max_length=1024, verbose_name='操作值')
    CheckType = models.CharField(max_length=1024,verbose_name='断言类型')
    CheckValue = models.CharField(max_length=1024,verbose_name='断言值')

    class Meta:
        db_table = 'bt_check_case'
        verbose_name = verbose_name_plural = '用例表'

    def __str__(self):
        return self.id


class KeyWord(models.Model):
    """关键字表"""
    id = models.AutoField(primary_key=True)
    key_word_name = models.CharField(max_length=1024,verbose_name='关键字名称')
    key_word_func = models.CharField(max_length=1024,verbose_name='关键字方法')

    class Meta:
        db_table = 'bt_key_word'
        verbose_name = verbose_name_plural = '关键字表'

    def __str__(self):
        return self.id