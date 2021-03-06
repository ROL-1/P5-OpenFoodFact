-- MySQL Script generated by MySQL Workbench
-- Wed Aug 12 11:24:15 2020
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema DBOFF1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema DBOFF1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `DBOFF1` DEFAULT CHARACTER SET utf8 ;
USE `DBOFF1` ;

-- -----------------------------------------------------
-- Table `DBOFF1`.`Brands`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOFF1`.`Brands` (
  `brands_id` INT NOT NULL AUTO_INCREMENT,
  `brands` VARCHAR(75) NOT NULL,
  PRIMARY KEY (`brands_id`),
  UNIQUE INDEX `brands_UNIQUE` (`brands` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DBOFF1`.`Codes_products_OFF`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOFF1`.`Codes_products_OFF` (
  `Codes_products_OFF_id` INT NOT NULL AUTO_INCREMENT,
  `code` BIGINT NOT NULL,
  PRIMARY KEY (`Codes_products_OFF_id`),
  UNIQUE INDEX `code_UNIQUE` (`code` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DBOFF1`.`Categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOFF1`.`Categories` (
  `categories_id` INT NOT NULL AUTO_INCREMENT,
  `categories` VARCHAR(75) NOT NULL,
  PRIMARY KEY (`categories_id`),
  UNIQUE INDEX `categories_UNIQUE` (`categories` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DBOFF1`.`Nutriscore_grades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOFF1`.`Nutriscore_grades` (
  `nutriscore_grade_id` INT NOT NULL AUTO_INCREMENT,
  `nutriscore_grade` CHAR(1) NOT NULL,
  UNIQUE INDEX `nutriscore_grade_UNIQUE` (`nutriscore_grade` ASC) VISIBLE,
  PRIMARY KEY (`nutriscore_grade_id`));


-- -----------------------------------------------------
-- Table `DBOFF1`.`Products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOFF1`.`Products` (
  `products_id` INT NOT NULL AUTO_INCREMENT,
  `Codes_products_OFF_Codes_products_OFF_id` INT NOT NULL,
  `product_name_fr` VARCHAR(100) NOT NULL,
  `generic_name_fr` VARCHAR(100) NOT NULL,
  `url` VARCHAR(150) NOT NULL,
  `Brands_brands_id` INT NOT NULL,
  `Nutriscore_grades_nutriscore_grade_id` INT NOT NULL,
  `Categories_categories_id` INT NOT NULL,
  PRIMARY KEY (`products_id`, `Codes_products_OFF_Codes_products_OFF_id`, `Brands_brands_id`, `Nutriscore_grades_nutriscore_grade_id`, `Categories_categories_id`),
  INDEX `fk_Products_Brands1_idx` (`Brands_brands_id` ASC) VISIBLE,
  INDEX `fk_Products_Codes_products_OFF1_idx` (`Codes_products_OFF_Codes_products_OFF_id` ASC) VISIBLE,
  UNIQUE INDEX `product_name_fr_UNIQUE` (`product_name_fr` ASC) VISIBLE,
  UNIQUE INDEX `url_UNIQUE` (`url` ASC) VISIBLE,
  INDEX `fk_Products_Categories1_idx` (`Categories_categories_id` ASC) VISIBLE,
  INDEX `fk_Products_Nutriscore_grades1_idx` (`Nutriscore_grades_nutriscore_grade_id` ASC) VISIBLE,
  CONSTRAINT `fk_Products_Brands1`
    FOREIGN KEY (`Brands_brands_id`)
    REFERENCES `DBOFF1`.`Brands` (`brands_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_Codes_products_OFF1`
    FOREIGN KEY (`Codes_products_OFF_Codes_products_OFF_id`)
    REFERENCES `DBOFF1`.`Codes_products_OFF` (`Codes_products_OFF_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_Categories1`
    FOREIGN KEY (`Categories_categories_id`)
    REFERENCES `DBOFF1`.`Categories` (`categories_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_Nutriscore_grades1`
    FOREIGN KEY (`Nutriscore_grades_nutriscore_grade_id`)
    REFERENCES `DBOFF1`.`Nutriscore_grades` (`nutriscore_grade_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `DBOFF1`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOFF1`.`Users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(25) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DBOFF1`.`Searches_saved`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOFF1`.`Searches_saved` (
  `searches_saved_id` INT NOT NULL AUTO_INCREMENT,
  `Products_products_id` INT NOT NULL,
  `substitute_id` INT NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `Users_user_id` INT NOT NULL,
  PRIMARY KEY (`searches_saved_id`, `Products_products_id`, `Users_user_id`),
  INDEX `fk_Searches_saved_Users1_idx` (`Users_user_id` ASC) VISIBLE,
  INDEX `fk_Searches_saved_Products1_idx` (`Products_products_id` ASC) VISIBLE,
  CONSTRAINT `fk_Searches_saved_Users1`
    FOREIGN KEY (`Users_user_id`)
    REFERENCES `DBOFF1`.`Users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Searches_saved_Products1`
    FOREIGN KEY (`Products_products_id`)
    REFERENCES `DBOFF1`.`Products` (`products_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `DBOFF1`.`Stores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOFF1`.`Stores` (
  `stores_id` INT NOT NULL AUTO_INCREMENT,
  `stores` VARCHAR(75) NOT NULL,
  PRIMARY KEY (`stores_id`),
  UNIQUE INDEX `stores_UNIQUE` (`stores` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `DBOFF1`.`Products_has_Stores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DBOFF1`.`Products_has_Stores` (
  `Products_products_id` INT NOT NULL,
  `Stores_stores_id` INT NOT NULL,
  PRIMARY KEY (`Products_products_id`, `Stores_stores_id`),
  INDEX `fk_Products_has_Stores_Stores1_idx` (`Stores_stores_id` ASC) VISIBLE,
  INDEX `fk_Products_has_Stores_Products1_idx` (`Products_products_id` ASC) VISIBLE,
  CONSTRAINT `fk_Products_has_Stores_Products1`
    FOREIGN KEY (`Products_products_id`)
    REFERENCES `DBOFF1`.`Products` (`products_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_has_Stores_Stores1`
    FOREIGN KEY (`Stores_stores_id`)
    REFERENCES `DBOFF1`.`Stores` (`stores_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
