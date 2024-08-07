CREATE TABLE `cluster` (
  `cluster_id` char(12) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `version` varchar(100) DEFAULT NULL,
  `cni_plugin` varchar(50) DEFAULT NULL,
  `delete_protection` tinyint(1) NOT NULL DEFAULT '0',
  `status_phase` varchar(50) NOT NULL,
  `status_condition_type` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cluster_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
