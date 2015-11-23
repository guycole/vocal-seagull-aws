SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `vocal_seagull` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `vocal_seagull` ;

-- -----------------------------------------------------
-- Table `vocal_seagull`.`observation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `vocal_seagull`.`observation` ;

CREATE  TABLE IF NOT EXISTS `vocal_seagull`.`observation` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `time_stamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,
  `station` VARCHAR(8) NOT NULL ,
  `location` VARCHAR(128) NOT NULL ,
  `latitude` VARCHAR(32) NOT NULL ,
  `longitude` VARCHAR(32) NOT NULL ,
  `rfc822` VARCHAR(64) NOT NULL ,
  `temp_c` VARCHAR(32) NOT NULL ,
  `temp_f` VARCHAR(32) NOT NULL ,
  `dewpoint_c` VARCHAR(32) NOT NULL ,
  `dewpoint_f` VARCHAR(32) NOT NULL ,
  `relative_humidity` VARCHAR(32) NOT NULL ,
  `visibility_mi` VARCHAR(32) NOT NULL ,
  `weather` VARCHAR(64) NOT NULL ,
  `wind_degrees` VARCHAR(32) NOT NULL ,
  `wind_kt` VARCHAR(32) NOT NULL ,
  `wind_mph` VARCHAR(32) NOT NULL ,
  `pressure_in` VARCHAR(32) NOT NULL ,
  `pressure_mb` VARCHAR(32) NOT NULL ,
  `heat_index_c` VARCHAR(32) NOT NULL ,
  `heat_index_f` VARCHAR(32) NOT NULL ,
  `windchill_c` VARCHAR(32) NOT NULL ,
  `windchill_f` VARCHAR(32) NOT NULL ,
  `wind_gust_kt` VARCHAR(32) NOT NULL ,
  `wind_gust_mph` VARCHAR(32) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;

USE `vocal_seagull` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
