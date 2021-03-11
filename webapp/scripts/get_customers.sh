#! /bin/bash


ssh -l root 192.168.200.13 "psql -d jiradb -U root -c \"\\copy (SELECT ji.issuenum, TRIM(cf.stringvalue) as phone, l.label FROM jiraissue ji JOIN label l ON ji.id = l.issue AND l.fieldid = 10203 JOIN customfieldvalue cf ON ji.id = cf.issue AND cf.customfield = 10401 AND LENGTH(cf.stringvalue) > 3 WHERE ji.project = 10104 ORDER BY ji.id ASC) To '/tmp/customers.csv' With csv DELIMITER ',' HEADER ENCODING 'UTF8';\""

scp root@192.168.200.13:/tmp/customers.csv /var/lib/mysql-files
sed -i "s/введите-имя-клиента/Фамилия,Имя/" /var/lib/mysql-files/customers.csv
sed -i "s/_/,/" /var/lib/mysql-files/customers.csv
sed -i "s/label/lastname,name/" /var/lib/mysql-files/customers.csv
sed -i "s/ //" /var/lib/mysql-files/customers.csv
sed -i "s/+//" /var/lib/mysql-files/customers.csv
sed -i "s/-//" /var/lib/mysql-files/customers.csv
sed -i "s/ //" /var/lib/mysql-files/customers.csv
sed -i "s/-//" /var/lib/mysql-files/customers.csv
sed -i "s/Планка/Планка,Имя/" /var/lib/mysql-files/customers.csv



mysql -u root webappdb -e "LOAD DATA INFILE '/var/lib/mysql-files/customers.csv' INTO TABLE customers FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 ROWS (issuenum,phone,lastname,name);"
