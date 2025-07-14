-- Database schema for Heptapal Agent Core
-- This script creates the necessary tables for reminders and todos

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `heptapal-db` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `heptapal-db`;

-- Create reminders table
CREATE TABLE IF NOT EXISTS `reminders` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT NOT NULL,
    `remind_time` DATETIME NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `is_active` BOOLEAN DEFAULT TRUE,
    INDEX `idx_title` (`title`),
    INDEX `idx_remind_time` (`remind_time`),
    INDEX `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create todos table
CREATE TABLE IF NOT EXISTS `todos` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `priority` ENUM('low', 'medium', 'high') DEFAULT 'medium',
    `status` ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    `due_date` DATE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `completed_at` DATETIME,
    INDEX `idx_title` (`title`),
    INDEX `idx_priority` (`priority`),
    INDEX `idx_status` (`status`),
    INDEX `idx_due_date` (`due_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert some sample data for testing
INSERT INTO `reminders` (`title`, `description`, `remind_time`, `is_active`) VALUES
('Team Meeting', 'Weekly team standup meeting', NOW() + INTERVAL 1 HOUR, TRUE),
('Project Deadline', 'Submit final project report', NOW() + INTERVAL 2 DAY, TRUE),
('Birthday Reminder', 'John\'s birthday celebration', NOW() + INTERVAL 1 WEEK, TRUE);

INSERT INTO `todos` (`title`, `description`, `priority`, `status`, `due_date`) VALUES
('Complete Documentation', 'Write API documentation for the new features', 'high', 'pending', DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Code Review', 'Review pull request #123 for the authentication module', 'medium', 'in_progress', DATE_ADD(CURDATE(), INTERVAL 1 DAY)),
('Setup Development Environment', 'Install and configure development tools', 'low', 'completed', CURDATE()),
('Plan Sprint', 'Plan tasks for the next sprint', 'medium', 'pending', DATE_ADD(CURDATE(), INTERVAL 5 DAY));

-- Show table structure
DESCRIBE `reminders`;
DESCRIBE `todos`;

-- Show sample data
SELECT 'Reminders:' as table_name;
SELECT * FROM `reminders`;

SELECT 'Todos:' as table_name;
SELECT * FROM `todos`; 