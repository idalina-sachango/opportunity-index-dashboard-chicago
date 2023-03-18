########################################
# CAPP 30122: tools4schools

# Import data from Urban Institute API
# and export for further processing in
# Python.

# Data sources:
# - Common Core of Data
# - Civil Rights Data Collection

# Requirements:
# install.packages('educationdata')
# devtools::install_github('UrbanInstitute/education-data-package-r')
########################################

rm(list = ls())
library(educationdata)
library(tidyverse)

# set directory
export_dir <- paste0("../../data/ccd_crdc/")

###############################################################
# User-Written Functions
###############################################################

# Keep variables with a common suffix and rename column names accordingly
keep_totals_only <- function(df, suffix, id_vars) {
  df <- df %>% select(all_of(id_vars), ends_with(suffix, ignore.case = TRUE))
  colnames(df) <- gsub(paste0("_", suffix), "", colnames(df), ignore.case = TRUE)
  return(df)
}


###############################################################
# 1. CCD Data
###############################################################
ccd_directory <- get_education_data(level = 'schools', 
                                    source = 'ccd', 
                                    topic = 'directory',
                                    filters = list(year = 2017,
                                                   fips = 17),
                                    add_labels = TRUE)

write_csv(ccd_directory, paste0(export_dir, "ccd_directory_2017.csv"))



###############################################################
# 2. CRDC Data
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


###############################################################
# 3. Consolidate CRDC datasets
###############################################################

crdc_vars = c("crdc_id","ncessch","year","fips","leaid")


#(a) Start with enrollment
consolidated <- keep_totals_only(crdc_enrollment, "total_total", crdc_vars)


#(b) staff
crdc_staff <- crdc_staff %>%
                select(all_of(crdc_vars), teachers_certified_fte, counselors_fte, law_enforcement_fte)
    
consolidated <- left_join(consolidated, crdc_staff, by = crdc_vars)


#(c) finance (teacher salaries)
crdc_finance <- crdc_finance %>%
                  select(all_of(crdc_vars), salaries_total) %>%
                  rename(salaries = salaries_total)

consolidated <- left_join(consolidated, crdc_finance, by = crdc_vars)

#(d) Advanced Placement Test Enrollment
crdc_ap_ib <- crdc_ap_ib %>%
                select(all_of(crdc_vars), ends_with("total_total", ignore.case = TRUE))
colnames(crdc_ap_ib)<-gsub("_total_total", "", colnames(crdc_ap_ib), ignore.case = TRUE)
consolidated <- left_join(consolidated, crdc_ap_ib, by = crdc_vars)
names(consolidated)[6:length(names(consolidated))] <- paste0(names(consolidated)[6:length(names(consolidated))],"_crdc")
write_csv(consolidated, paste0(export_dir, "/crdc_data_2017.csv"))