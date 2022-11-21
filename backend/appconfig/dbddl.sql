
CREATE TABLE `credential` (
	`credential_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(50) NOT NULL, 
	`description` VARCHAR(100), 
	`organization_id` INTEGER(11), 
	`credential_type_id` INTEGER(11), 
	`awx_credential_id` INTEGER(11), 
	`created` VARCHAR(50), 
	`modified` VARCHAR(50), 
	PRIMARY KEY  `(credential_id`) , 
	CONSTRAINT `credential_FK` FOREIGN KEY `(credential_type_id`)  REFERENCES credential_type  `(credential_type_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `credential_type` (
	`credential_type_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(50) NOT NULL, 
	`description` VARCHAR(100), 
	`kind` VARCHAR(50), 
	`awx_credential_type_id` INTEGER(11), 
	`created` VARCHAR(50), 
	`modified` VARCHAR(50), 
	PRIMARY KEY  `(credential_type_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `git_repo` (
	`git_repo_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(50) NOT NULL, 
	`description` VARCHAR(100), 
	`default_branch` VARCHAR(50), 
	`private` TINYINT(1), 
	`html_url` VARCHAR(100), 
	`ssh_url` VARCHAR(100), 
	`clone_url` VARCHAR(100), 
	`owner` VARCHAR(20), 
	`gitea_repo_id` INTEGER(11), 
	PRIMARY KEY  `(git_repo_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `host` (
	`host_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(50) NOT NULL, 
	`description` VARCHAR(100), 
	`enabled` TINYINT(1), 
	`ip` VARCHAR(50), 
	`username` VARCHAR(50), 
	`password` VARCHAR(100), 
	`awx_host_id` INTEGER(11), 
	`created` VARCHAR(50), 
	`modified` VARCHAR(50), 
	`tag` VARCHAR(20), 
	PRIMARY KEY  `(host_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `host_inventory` (
	`id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`host_id` INTEGER(11), 
	`inventory_id` INTEGER(11), 
	PRIMARY KEY  `(id`) , 
	CONSTRAINT `host_inventory_FK` FOREIGN KEY `(host_id`)  REFERENCES host  `(host_id`) , 
	CONSTRAINT `host_inventory_FK_1` FOREIGN KEY `(inventory_id`)  REFERENCES inventory  `(inventory_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `inventory` (
	`inventory_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(50) NOT NULL, 
	`description` VARCHAR(100), 
	`organization_id` INTEGER(11), 
	`kind` VARCHAR(20), 
	`awx_inventory_id` VARCHAR(100), 
	`created` VARCHAR(50), 
	`modified` VARCHAR(50), 
	PRIMARY KEY  `(inventory_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `job` (
	`job_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(50) NOT NULL, 
	`description` VARCHAR(100), 
	`unified_job_template` INTEGER(11), 
	`launch_type` VARCHAR(50), 
	`status` VARCHAR(20), 
	`failed` TINYINT(1), 
	`started` VARCHAR(50), 
	`finished` VARCHAR(50), 
	`canceled_on` VARCHAR(50), 
	`elapsed` VARCHAR(50), 
	`job_template_id` INTEGER(11), 
	`awx_job_id` INTEGER(11), 
	PRIMARY KEY  `(job_id`) , 
	CONSTRAINT `job_FK` FOREIGN KEY `(job_template_id`)  REFERENCES job_template  `(job_template_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `job_template` (
	`job_template_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(50) NOT NULL, 
	`description` VARCHAR(100), 
	`job_type` VARCHAR(20), 
	`inventory_id` INTEGER(11), 
	`project_id` INTEGER(11), 
	`playbook` VARCHAR(100), 
	`scm_branch` VARCHAR(50), 
	`forks` INTEGER(11), 
	`limit` VARCHAR(100), 
	`verbosity` INTEGER(11), 
	`job_tags` VARCHAR(100), 
	`timeout` INTEGER(11), 
	`job_slice_count` INTEGER(11), 
	`awx_job_template_id` INTEGER(11), 
	`extra_vars` LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin, 
	`created` VARCHAR(50), 
	`modified` VARCHAR(50), 
	`last_job_run` VARCHAR(50), 
	`last_job_failed` TINYINT(1), 
	`next_job_run` VARCHAR(50), 
	`status` VARCHAR(20), 
	`type` VARCHAR(20), 
	`level` INTEGER(11), 
	PRIMARY KEY  `(job_template_id`) , 
	CONSTRAINT `job_template_FK` FOREIGN KEY `(inventory_id`)  REFERENCES inventory  `(inventory_id`) , 
	CONSTRAINT `job_template_FK_1` FOREIGN KEY `(project_id`)  REFERENCES project  `(project_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `playbook` (
	`playbook_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(50) NOT NULL, 
	`description` VARCHAR(100), 
	`path` VARCHAR(20) NOT NULL, 
	`git_repo_id` INTEGER(11) NOT NULL, 
	`tag` VARCHAR(50), 
	`download_url` VARCHAR(100), 
	`sha` VARCHAR(100), 
	`type` VARCHAR(50), 
	PRIMARY KEY  `(playbook_id`) , 
	CONSTRAINT `playbook_FK` FOREIGN KEY `(git_repo_id`)  REFERENCES git_repo  `(git_repo_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `project` (
	`project_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(50) NOT NULL, 
	`description` VARCHAR(100), 
	`scm_type` VARCHAR(20), 
	`scm_url` VARCHAR(100), 
	`scm_branch` VARCHAR(50), 
	`credential_id` INTEGER(11), 
	`organization_id` INTEGER(11), 
	`allow_override` TINYINT(1), 
	`created` VARCHAR(50), 
	`modified` VARCHAR(50), 
	`status` VARCHAR(20), 
	`awx_project_id` INTEGER(11), 
	`git_repo_id` INTEGER(11), 
	PRIMARY KEY  `(project_id`) , 
	CONSTRAINT `project_FK` FOREIGN KEY `(credential_id`)  REFERENCES credential  `(credential_id`) , 
	CONSTRAINT `project_FK_1` FOREIGN KEY `(git_repo_id`)  REFERENCES git_repo  `(git_repo_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB


CREATE TABLE `schedule` (
	`schedule_id` INTEGER(11) NOT NULL AUTO_INCREMENT, 
	`rrule` VARCHAR(200), 
	`cron` VARCHAR(100), 
	`job_template_id` INTEGER(11), 
	`name` VARCHAR(50), 
	`description` VARCHAR(100), 
	`enabled` TINYINT(1), 
	`extra_data` LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin, 
	`awx_schedule_id` INTEGER(11), 
	`created` VARCHAR(50), 
	`modified` VARCHAR(50), 
	PRIMARY KEY  `(schedule_id`) , 
	CONSTRAINT `schedule_FK` FOREIGN KEY `(job_template_id`)  REFERENCES job_template  `(job_template_id`) 
)DEFAULT CHARSET=utf8mb4 ENGINE=InnoDB

