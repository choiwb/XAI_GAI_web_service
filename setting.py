


# import psycopg2 as pg2
# import os
# import pandas as pd
# import torch
# from transformers import AutoTokenizer, pipeline

import re
import pickle
import itertools

SERVER_IP = '127.0.0.1'
PORT = 17171


# 2023/03/13 IPS 모델 - Light GBM
new_IPS_model_path = 'save_model/DSS_IPS_LGB_20230313.pkl'
# 위 모델을, SHAP의 TreeExplainer 연산 및 저장
IPS_explainer_path = 'save_model/DSS_IPS_LGB_explainer_20230313.pkl'

IPS_model = pickle.load(open(new_IPS_model_path, 'rb'))


# 2023/03/13 WAF 모델 - Light GBM
new_WAF_model_path = 'save_model/DSS_WAF_LGB_20230313.pkl'
# 위 모델을, SHAP의 TreeExplainer 연산 및 저장
WAF_explainer_path = 'save_model/DSS_WAF_LGB_explainer_20230313.pkl'

WAF_model = pickle.load(open(new_WAF_model_path, 'rb'))


# 2023/04/04 WEB 모델 - Light GBM
WEB_model_path = 'save_model/DSS_WEB_LGB_20230404.pkl'
# 위 모델을, SHAP의 TreeExplainer 연산 및 저장
WEB_explainer_path = 'save_model/DSS_WEB_LGB_explainer_20230404.pkl'

WEB_model = pickle.load(open(WEB_model_path, 'rb'))



ips_query = """
    
    SELECT
   
        IF(INT(RLIKE(payload, 'VCAvY2dpLWJpbi9waHA0') )>0
        OR INT(RLIKE(payload, 'L2NnaS1iaW4v') )>0
        OR INT(RLIKE(payload, 'IC9jZ2ktYmlu') )>0
        OR INT(RLIKE(payload, 'UE9TVCAvY2dpLWJpbi9waHA/') )>0
        OR INT(RLIKE(payload, 'VCAvY2dpLWJpbi9w') )>0
        OR INT(RLIKE(payload, 'ZGllKEBtZDU=') )>0
        OR INT(RLIKE(payload, 'L2FueWZvcm0yL3VwZGF0ZS9hbnlmb3JtMi5pbmk=') )>0
        OR INT(RLIKE(payload, 'Ly5iYXNoX2hpc3Rvcnk=') )>0
        OR INT(RLIKE(payload, 'L2V0Yy9wYXNzd2Q=') )>0
        OR INT(RLIKE(payload, 'QUFBQUFBQUFBQQ==') )>0
        OR INT(RLIKE(payload, 'IG1hc3NjYW4vMS4w') )>0
        OR INT(RLIKE(payload, 'd2dldA==') )>0
        OR INT(RLIKE(payload, 'MjB3YWl0Zm9yJTIwZGVsYXklMjAn') )>0
        OR INT(RLIKE(payload, 'V0FJVEZPUiBERUxBWQ==') )>0
        OR INT(RLIKE(payload, 'ZXhlYw==') )>0
        OR INT(RLIKE(payload, 'Tm9uZQ==') )>0
        OR INT(RLIKE(payload, 'OyB3Z2V0') )>0
        OR INT(RLIKE(payload, 'VXNlci1BZ2VudDogRGlyQnVzdGVy') )>0
        OR INT(RLIKE(payload, 'cGhwIGRpZShAbWQ1') )>0
        OR INT(RLIKE(payload, 'JTI4U0VMRUNUJTIw') )>0
                ,1, 0) AS ips_00001_payload_base64,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)from') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)count') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)distinct') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'union(.*?)select') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)extractvalue(.*?)xmltype') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'from(.*?)generate(.*?)series') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'from(.*?)group(.*?)by') )>0
                ,1, 0) AS ips_00001_payload_sql_comb_01,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'case(.*?)when') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'then(.*?)else') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'like') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'sleep') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'delete') )>0
                ,1, 0) AS ips_00001_payload_sql_comb_02,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'waitfor(.*?)delay') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'db(.*?)sql(.*?)server') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'cast(.*?)chr') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'upper(.*?)xmltype') )>0
                ,1, 0) AS ips_00001_payload_sql_comb_03,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'script(.*?)alert') )>0
        OR INT(RLIKE(LOWER(payload), 'eval') )>0
                ,1, 0) AS ips_00001_payload_xss_comb_01,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'wget(.*?)ttp') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'chmod(.*?)777') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'rm(.*?)rf') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'cd(.*?)tmp') )>0
                ,1, 0) AS ips_00001_payload_cmd_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'jndi(.*?)dap') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '),'jndi(.*?)dns') )>0
                ,1, 0) AS ips_00001_payload_log4j_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'etc(.*?)passwd') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)createelement') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cgi(.*?)bin') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)forms') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)location') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'fckeditor(.*?)filemanager') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'manager(.*?)html') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'current_config(.*?)passwd') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'currentsetting(.*?)htm') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'well(.*?)known') )>0
                ,1, 0) AS ips_00001_payload_word_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'bash(.*?)history') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'apache(.*?)struts') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)open') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'backup(.*?)sql') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'robots(.*?)txt') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'sqlexec(.*?)php') )>0
        OR INT(RLIKE(LOWER(payload), 'htaccess') )>0
        OR INT(RLIKE(LOWER(payload), 'htpasswd') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cgi(.*?)cgi') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'api(.*?)ping') )>0
                ,1, 0) AS ips_00001_payload_word_comb_02,

        IF(INT(RLIKE(LOWER(payload), 'aaaaaaaaaa') )>0
        OR INT(RLIKE(LOWER(payload), 'cacacacaca') )>0
        OR INT(RLIKE(LOWER(payload), 'mozi[\\.]') )>0
        OR INT(RLIKE(LOWER(payload), 'bingbot') )>0
        OR INT(RLIKE(LOWER(payload), 'md5') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'count(.*?)cgi(.*?)http') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'this(.*?)program(.*?)can') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'get(.*?)ping') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'msadc(.*?)dll(.*?)http') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'filename(.*?)asp') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'filename(.*?)jsp') )>0
        OR INT(RLIKE(LOWER(payload), 'powershell'))>0
        OR INT(RLIKE(LOWER(payload), '[\\.]env'))>0
                ,1, 0) AS ips_00001_payload_word_comb_03,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp-login') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp-content') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp-include') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp-config') )>0
                ,1, 0) AS ips_00001_payload_wp_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cmd(.*?)open') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'echo(.*?)shellshock') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'php(.*?)echo') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'admin(.*?)php') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'script(.*?)setup(.*?)php') )>0
        OR INT(RLIKE(LOWER(payload), 'phpinfo') )>0
        OR INT(RLIKE(LOWER(payload), 'administrator') )>0
        OR INT(RLIKE(LOWER(payload), 'phpmyadmin') )>0
        OR INT(RLIKE(LOWER(payload), 'access') )>0
        OR INT(RLIKE(LOWER(payload), 'mdb') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wise(.*?)survey(.*?)admin') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'admin(.*?)serv(.*?)admpw') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'php(.*?)create(.*?)function') )>0
                ,1, 0) AS ips_00001_payload_word_comb_04,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)zgrab') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)nmap') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)dirbuster') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)ahrefsbot') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)baiduspider') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)mj12bot') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)petalbot') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)curl/') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)semrushbot') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)masscan') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)sqlmap') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)urlgrabber(.*?)yum') )>0
                ,1, 0) AS ips_00001_payload_useragent_comb,
                
        (SIZE(SPLIT(REGEXP_REPLACE(payload, '\\n|\\r|\\t', ' '), 'GET(.*?)HTTP/1.')) -1)
            + (SIZE(SPLIT(REGEXP_REPLACE(payload, '\\n|\\r|\\t', ' '), 'POST(.*?)HTTP/1.')) -1)
        + (SIZE(SPLIT(REGEXP_REPLACE(payload, '\\n|\\r|\\t', ' '), 'HEAD(.*?)HTTP/1.')) -1)
        + (SIZE(SPLIT(REGEXP_REPLACE(payload, '\\n|\\r|\\t', ' '), 'OPTION(.*?)HTTP/1.')) -1)
        AS ips_00001_payload_whitelist

    FROM table
    
"""

waf_query = """
    
    SELECT
   
        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)from') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)count') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)distinct') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'union(.*?)select') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)extractvalue(.*?)xmltype') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'from(.*?)generate(.*?)series') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'from(.*?)group(.*?)by') )>0
                ,1, 0) AS waf_00001_payload_sql_comb_01,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'case(.*?)when') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'then(.*?)else') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'like') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'sleep') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'delete') )>0
                ,1, 0) AS waf_00001_payload_sql_comb_02,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'waitfor(.*?)delay') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'db(.*?)sql(.*?)server') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'cast(.*?)chr') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'upper(.*?)xmltype') )>0
                ,1, 0) AS waf_00001_payload_sql_comb_03,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'script(.*?)alert') )>0
        OR INT(RLIKE(LOWER(payload), 'eval') )>0
                ,1, 0) AS waf_00001_payload_xss_comb_01,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'wget(.*?)ttp') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'chmod(.*?)777') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'rm(.*?)rf') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'cd(.*?)tmp') )>0
                ,1, 0) AS waf_00001_payload_cmd_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'jndi(.*?)dap') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '),'jndi(.*?)dns') )>0
                ,1, 0) AS waf_00001_payload_log4j_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'etc(.*?)passwd') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)createelement') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cgi(.*?)bin') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)forms') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)location') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'fckeditor(.*?)filemanager') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'manager(.*?)html') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'current_config(.*?)passwd') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'currentsetting(.*?)htm') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'well(.*?)known') )>0
                ,1, 0) AS waf_00001_payload_word_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'bash(.*?)history') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'apache(.*?)struts') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'document(.*?)open') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'backup(.*?)sql') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'robots(.*?)txt') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'sqlexec(.*?)php') )>0
        OR INT(RLIKE(LOWER(payload), 'htaccess') )>0
        OR INT(RLIKE(LOWER(payload), 'htpasswd') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cgi(.*?)cgi') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'api(.*?)ping') )>0
                ,1, 0) AS waf_00001_payload_word_comb_02,

        IF(INT(RLIKE(LOWER(payload), 'aaaaaaaaaa') )>0
        OR INT(RLIKE(LOWER(payload), 'cacacacaca') )>0
        OR INT(RLIKE(LOWER(payload), 'mozi[\\.]') )>0
        OR INT(RLIKE(LOWER(payload), 'bingbot') )>0
        OR INT(RLIKE(LOWER(payload), 'md5') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'count(.*?)cgi(.*?)http') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'this(.*?)program(.*?)can') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'get(.*?)ping') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'msadc(.*?)dll(.*?)http') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'filename(.*?)asp') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'filename(.*?)jsp') )>0
        OR INT(RLIKE(LOWER(payload), 'powershell'))>0
        OR INT(RLIKE(LOWER(payload), '[\\.]env'))>0
                ,1, 0) AS waf_00001_payload_word_comb_03,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp-login') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp-content') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp-include') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wp-config') )>0
                ,1, 0) AS waf_00001_payload_wp_comb_01,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'cmd(.*?)open') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'echo(.*?)shellshock') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'php(.*?)echo') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'admin(.*?)php') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'script(.*?)setup(.*?)php') )>0
        OR INT(RLIKE(LOWER(payload), 'phpinfo') )>0
        OR INT(RLIKE(LOWER(payload), 'administrator') )>0
        OR INT(RLIKE(LOWER(payload), 'phpmyadmin') )>0
        OR INT(RLIKE(LOWER(payload), 'access') )>0
        OR INT(RLIKE(LOWER(payload), 'mdb') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'wise(.*?)survey(.*?)admin') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'admin(.*?)serv(.*?)admpw') )>0
        OR INT(RLIKE(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'php(.*?)create(.*?)function') )>0
                ,1, 0) AS waf_00001_payload_word_comb_04,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)zgrab') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)nmap') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)dirbuster') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)ahrefsbot') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)baiduspider') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)mj12bot') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)petalbot') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)curl/') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)semrushbot') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)masscan') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)sqlmap') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(payload), '\\n|\\r|\\t', ' '), 'http/1.', 2)[1],  'user(.*?)agent(.*?)urlgrabber(.*?)yum') )>0
                ,1, 0) AS waf_00001_payload_useragent_comb
        
    FROM table
    """


web_query = """

SELECT 

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)from') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)count') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)concat') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)distinct') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'union(.*?)select') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'select(.*?)extractvalue(.*?)xmltype') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'from(.*?)generate(.*?)series') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'from(.*?)group(.*?)by') )>0
                ,1, 0) AS weblog_sql_comb_01,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'case(.*?)when') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'then(.*?)else') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'like') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'sleep') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'delete(.*?)from') )>0
                ,1, 0) AS weblog_sql_comb_02,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'where_framework') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'sql_server') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'order=1') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'id=0') )>0
                ,1, 0) AS weblog_sql_comb_03,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'waitfor(.*?)delay') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'db(.*?)sql(.*?)server') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'cast(.*?)chr') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'upper(.*?)xmltype') )>0
                ,1, 0) AS weblog_sql_comb_04,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'sql(.*?)select') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'query(.*?)select') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  '=yes') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  '=true') )>0
                ,1, 0) AS weblog_sql_comb_05,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'script(.*?)alert') )>0
        OR INT(RLIKE(LOWER(web_log), 'onmouseover') )>0
        OR INT(RLIKE(LOWER(web_log), 'eval') )>0
                ,1, 0) AS weblog_xss_comb_01,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'wget(.*?)ttp') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'chmod(.*?)777') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'rm(.*?)-rf') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'cd(.*?)tmp') )>0
                ,1, 0) AS weblog_cmd_comb_01,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'syscmd(.*?)cmd') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'exec(.*?)cmd(.*?)dir') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'exec(.*?)cmd(.*?)ls') )>0
                ,1, 0) AS weblog_cmd_comb_02,

        IF(INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'command') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'ping%20') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'ping[\\+]') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'echo%20') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'echo[\\+]') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'cat%20') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'cat[\\+]') )>0
        OR INT(RLIKE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'http/1.', 2)[0],  'shell_exe') )>0
                ,1, 0) AS weblog_cmd_comb_03,

        IF(INT(RLIKE(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), 'etc(.*?)passwd') )>0
                ,1, 0) AS weblog_dir_access_comb_01,

        (SIZE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), '[\\.][\\.]/')) -1)
        + (SIZE(SPLIT(REGEXP_REPLACE(LOWER(web_log), '\\n|\\r|\\t', ' '), '[\\.][\\.]%2f')) -1)
                AS weblog_dir_access_comb_02


FROM table

"""




# new_sql_query의 ips_00001_payload_base64 부터 ips_00001_payload_useragent_comb 까지 추출
# re.S의 경우, 줄바꿈 문자열 까지 매치 !!!!!!!
# attack_new_sql_query = re.findall(r'ips_00001_payload_base64.*?ips_00001_payload_useragent_comb', ips_query, re.S)[0]
# attack_new_sql_query '\\n|\\r|\\t', 'http/1.', 2 는 제거, 단 regex = False
attack_query = waf_query.replace('\\n|\\r|\\t', '').replace("'http/1.', 2", '')
# new_sql_query의 '' 안에 있는 문자열들을 추출하여 리스트 생성, 
ai_field = re.findall(r'\'(.*?)\'', attack_query)
# ai_field에서 'remove_string' 는 제거
ai_field = [x for x in ai_field if x != '' and x != ' ']


# attack_new_sql_query 에서 'AS' 를 기준으로 분할
attack_new_sql_query_split = attack_query.split('AS')

sql_1, sql_2, sql_3, xss, cmd, log4j, word_1, word_2, word_3, wp, word_4, user_agent = attack_new_sql_query_split[:12]
sql_1, sql_2, sql_3, xss, cmd, log4j, word_1, word_2, word_3, wp, word_4, user_agent = list(map(lambda x: re.findall(r'\'(.*?)\'', x), 
                                                                        [sql_1, sql_2, sql_3, xss, cmd, log4j, word_1, word_2, word_3, wp, word_4, user_agent]))
sql_1, sql_2, sql_3, xss, cmd, log4j, word_1, word_2, word_3, wp, word_4, user_agent = list(map(lambda x: [y for y in x if y != '' and y != ' '],
                                                                        [sql_1, sql_2, sql_3, xss, cmd, log4j, word_1, word_2, word_3, wp, word_4, user_agent])) 


# attack_new_sql_query '\\n|\\r|\\t', 'http/1.', 2 는 제거, 단 regex = False
web_attack_query = web_query.replace('\\n|\\r|\\t', '').replace("'http/1.', 2", '')
# new_sql_query의 '' 안에 있는 문자열들을 추출하여 리스트 생성, 
web_ai_field = re.findall(r'\'(.*?)\'', web_attack_query)
# ai_field에서 'remove_string' 는 제거
web_ai_field = [x for x in web_ai_field if x != '' and x != ' ']

# web_attack_new_sql_query_split 에서 'AS' 를 기준으로 분할
web_attack_new_sql_query_split = web_attack_query.split('AS')

web_sql_1, web_sql_2, web_sql_3, web_sql_4, web_sql_5, web_xss, web_cmd_1, web_cmd_2, web_cmd_3, dir_access_1, dir_access_2 = web_attack_new_sql_query_split[:11]
web_sql_1, web_sql_2, web_sql_3, web_sql_4, web_sql_5, web_xss, web_cmd_1, web_cmd_2, web_cmd_3, dir_access_1, dir_access_2 = list(map(lambda x: re.findall(r'\'(.*?)\'', x), 
                                                                        [web_sql_1, web_sql_2, web_sql_3, web_sql_4, web_sql_5, web_xss, web_cmd_1, web_cmd_2, web_cmd_3, dir_access_1, dir_access_2]))
web_sql_1, web_sql_2, web_sql_3, web_sql_4, web_sql_5, web_xss, web_cmd_1, web_cmd_2, web_cmd_3, dir_access_1, dir_access_2 = list(map(lambda x: [y for y in x if y != '' and y != ' '],
                                                                        [web_sql_1, web_sql_2, web_sql_3, web_sql_4, web_sql_5, web_xss, web_cmd_1, web_cmd_2, web_cmd_3, dir_access_1, dir_access_2])) 


