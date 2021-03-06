BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `token` (
	`token`	TEXT
);
CREATE TABLE IF NOT EXISTS `agenda_item` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`agenda_id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`status`	INTEGER NOT NULL,
	FOREIGN KEY(`agenda_id`) REFERENCES `agenda`(`id`) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS `agenda` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`user_id`	INTEGER NOT NULL,
	`title`	TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS `user_id_title_unique` ON `agenda` (
	`user_id`,
	`title`	ASC
);
COMMIT;
