from lib.filters import *
from lib.pipeline.credential_pipeline import CredentialPipeline
from lib.rules import *


admin_default = CredentialPipeline(login_filter=(TagFilter('admin') | TagFilter('company')),
                                                       password_filter=TagFilter('admin'))
admin_company = CredentialPipeline(login_filter=TagFilter('admin'),
                                                       password_filter=TagFilter('company'),
                                                       password_chains=[
                                                           [],
                                                           [TagFilter('company'), AppendLastYearsRule(separators=(".", "", "@", "#", "!"))],
                                                           [TagFilter('company'), CapitalizeRule(), AppendLastYearsRule(separators=(".", "", "@", "#", "!"))],
                                                           ])
admin_keywords = CredentialPipeline(login_filter=TagFilter('admin'),
                                                       password_filter=TagFilter('keyword'),
                                                       password_chains=[
                                                           [],
                                                           [AppendLastYearsRule(separators=(".", "", "@", "#", "!"))],
                                                           [CapitalizeRule(), AppendLastYearsRule(separators=(".", "", "@", "#", "!"))],
                                                           ])
 
