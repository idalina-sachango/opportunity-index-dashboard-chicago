#Author: Nivedita Vatsa

rm(list = ls())
#install.packages('educationdata')
#devtools::install_github('UrbanInstitute/education-data-package-r')
library(educationdata)
library(tidyverse)


root <- "C:/Users/nived/OneDrive - The University of Chicago/Academic/Winter 2021/CS 122/Project"
output <- paste0(root,"/Output")
data_dir<- paste0(root,"/Data")

`%notin%` <- Negate(`%in%`)

###############################################################
#1. CCD Data
###############################################################
#(1a) ccd: directory
ccd_directory <- get_education_data(level = 'schools', 
                                    source = 'ccd', 
                                    topic = 'directory',
                                    filters = list(year = 2017,
                                                   fips = 17),
                                    add_labels = TRUE)

write_csv(ccd_directory, paste0(data_dir, "/ccd_directory_2017.csv"))

#(1b) ccd: school enrollment by race and sex
ccd_enrollment <- get_education_data(level = 'schools', 
                                 source = 'ccd', 
                                 topic = 'enrollment', 
                                 subtopic = list('race', 'sex'),
                                 filters = list(year = 2017,
                                                grade = 9:12,
                                                fips = 17),
                                 add_labels = TRUE)


ccd_enrollment <- ccd_enrollment %>%
                    group_by(year, ncessch, ncessch_num, race, sex, fips, leaid) %>%
                    summarise(enrollment = sum(enrollment, na.rm = TRUE)) %>% ungroup() %>% 
                    mutate(enrollment = ifelse(is.na(enrollment), 0, enrollment)) %>%
                    pivot_wider(names_from = c("race","sex"),
                                values_from = "enrollment")


#(1c) ccd: finance
ccd_finance <- get_education_data(level = 'school-districts', 
                                  source = 'ccd', 
                                  topic = 'finance',
                                  filters = list(year = 2017,
                                                 fips = 17),
                                  add_labels = TRUE)


###############################################################
#2. CRDC Data
###############################################################

#(2a) crdc: enrollment
crdc_enrollment <- get_education_data(level = 'schools', 
                                  source = 'crdc', 
                                  topic = 'enrollment',
                                  subtopic = c('race', 'sex'),
                                  filters = list(year = 2017,
                                                 fips = 17),
                                  add_labels = TRUE)

crdc_enrollment <- crdc_enrollment %>% 
                          select(-psenrollment_crdc) %>%
                          pivot_wider(names_from = c("race","sex"),
                                      values_from = "enrollment_crdc",
                                      names_prefix = "enrollment_") %>%
                          filter(ncessch == crdc_id)

  #sanity checks
  #dupes <- crdc_enroll_race_sex %>% group_by(ncessch) %>% filter(n()>1)
  #mismatches <- crdc_enroll_race_sex %>% filter(ncessch != crdc_id)
  only_in_ccd = setdiff(ccd_directory$ncessch, crdc_enrollment$ncessch)
  ccd_directory_xcrcd = ccd_directory %>% filter(ncessch %in% only_in_ccd)

#(2b) crdc: retention
# crdc_retention <- get_education_data(level = 'schools', 
#                                      source = 'crdc', 
#                                      topic = 'retention',
#                                      subtopic = c('race', 'sex'),
#                                      filters = list(year = 2017,
#                                                     grade = 9:12,
#                                                     fips = 17),
#                                      add_labels = TRUE)
# 
# 
# crdc_retention <- crdc_retention %>% 
#                      pivot_wider(names_from = c("race","sex", "grade"),
#                                  values_from = "students_retained") %>%
#                      filter(crdc_id == ncessch)
 
#(2c) crdc: teachers and staff
crdc_staff <- get_education_data(level = 'schools', 
                                      source = 'crdc', 
                                      topic = 'teachers-staff',
                                      filters = list(year = 2017,
                                                     fips = 17),
                                      add_labels = TRUE)

crdc_staff <- crdc_staff %>% filter(crdc_id == ncessch)

#(2d) crdc: finance
crdc_finance <- get_education_data(level = 'schools', 
                                   source = 'crdc', 
                                   topic = 'school-finance',
                                   filters = list(year = 2017,
                                                  fips = 17),
                                   add_labels = TRUE)

crdc_finance <- crdc_finance %>% filter(crdc_id == ncessch)


#(2e) crdc: AP and IB
crdc_ap_ib <- get_education_data(level = 'schools', 
                                  source = 'crdc', 
                                  topic = 'ap-ib-enrollment',
                                  subtopic = c('race', 'sex'),
                                  filters = list(year = 2017,
                                                 fips = 17),
                                  add_labels = TRUE) %>%
                                  select(-ends_with(c("_IB","_gifted_talented"))) 

for(col in names(crdc_ap_ib)[grep("enrl_", names(crdc_ap_ib))]){
  crdc_ap_ib[[col]] = ifelse(is.na(crdc_ap_ib[[col]]), 0, 
                             ifelse(crdc_ap_ib[[col]] == -2, 0, 
                                    crdc_ap_ib[[col]]))}

crdc_ap_ib <- crdc_ap_ib %>%
                  pivot_wider(names_from = c("race","sex"),
                              values_from = starts_with("enrl_")) %>%
                  filter(crdc_id == ncessch)


#(2f) crdc: SAT and ACT
crdc_sat_act <- get_education_data(level = 'schools', 
                                 source = 'crdc', 
                                 topic = 'sat-act-participation',
                                 subtopic = c('race', 'sex'),
                                 filters = list(year = 2017,
                                                fips = 17),
                                 add_labels = TRUE)
crdc_sat_act <- crdc_sat_act %>% 
                  pivot_wider(names_from = c("race","sex"),
                              values_from = c("students_SAT_ACT")) %>%
                  filter(crdc_id == ncessch)

#(2g) crdc: credit recovery
crdc_credit_recovery <- get_education_data(level = 'schools', 
                                           source = 'crdc', 
                                           topic = 'credit-recovery',
                                           filters = list(year = 2017,
                                                          fips = 17),
                                           add_labels = TRUE)
crdc_credit_recovery <- crdc_credit_recovery %>% filter(crdc_id == ncessch)


# #(2h) crdc: AP exams
# crdc_ap_exams <- get_education_data(level = 'schools', 
#                                  source = 'crdc', 
#                                  topic = 'ap-exams',
#                                  subtopic = c('race', 'sex'),
#                                  filters = list(year = 2017,
#                                                 fips = 17),
#                                  add_labels = TRUE)
# crdc_ap_exams <- crdc_ap_exams %>% 
#                       pivot_wider(names_from = c("race","sex"),
#                                   values_from = starts_with("students_AP_")) %>%
#                       filter(crdc_id == ncessch)
# 
# 
# #(2i) crdc: math & science
# crdc_math_sci <- get_education_data(level = 'schools', 
#                                     source = 'crdc', 
#                                     topic = 'math-and-science',
#                                     subtopic = c('race', 'sex'),
#                                     filters = list(year = 2017,
#                                                    fips = 17),
#                                     add_labels = TRUE)
# crdc_math_sci <- crdc_math_sci %>% 
#                     pivot_wider(names_from = c("race","sex"),
#                                 values_from = starts_with("enrl_")) %>%
#                                 filter(crdc_id == ncessch)


###############################################################
#3. Consolidate CRDC atr
###############################################################

crdc_vars = c("crdc_id","ncessch","year","fips","leaid")
keep_totals_only <- function(df, suffix, id_vars){
  df <- df %>% select(all_of(id_vars), ends_with(suffix, ignore.case = TRUE))
  colnames(df) <- gsub(paste0("_", suffix), "", colnames(df), ignore.case = TRUE)
  return(df)
}


#(a) Start with enrollment
consolidated <- keep_totals_only(crdc_enrollment, "total_total", crdc_vars)

# crdc_enrollment <- crdc_enrollment %>% 
#                   select(all_of(crdc_vars), ends_with("total_total", ignore.case = TRUE))
# colnames(crdc_enrollment) <- gsub("_total_total", "", colnames(crdc_enrollment), ignore.case = TRUE)
# consolidated <- crdc_enrollment

#(b) staff
crdc_staff <- crdc_staff %>%
                select(all_of(crdc_vars), teachers_certified_fte, counselors_fte, law_enforcement_fte)
    
consolidated <- left_join(consolidated, crdc_staff, by = crdc_vars)


#(c) finance (teacher salaries)
crdc_finance <- crdc_finance %>%
                  select(all_of(crdc_vars), salaries_total) %>%
                  rename(salaries = salaries_total)

consolidated <- left_join(consolidated, crdc_finance, by = crdc_vars)

#(d) AP
crdc_ap_ib <- crdc_ap_ib %>%
                select(all_of(crdc_vars), ends_with("total_total", ignore.case = TRUE))
colnames(crdc_ap_ib)<-gsub("_total_total", "", colnames(crdc_ap_ib), ignore.case = TRUE)
consolidated <- left_join(consolidated, crdc_ap_ib, by = crdc_vars)
names(consolidated)[6:length(names(consolidated))] <- paste0(names(consolidated)[6:length(names(consolidated))],"_crdc")
write_csv(consolidated, paste0(output, "/crdc_data_2017.csv"))


# # Per-student statistics
# for(col in colnames(consolidated)){
#   if(col %notin% c(crdc_vars, "enrollment")){
#     consolidated[[col]] = (10^3) * as.numeric(consolidated[[col]]) / as.numeric(consolidated$enrollment)
#   }
# }


