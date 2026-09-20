-- MySQL 8.0+. Fictional company; all numeric inputs synthetic.
CREATE DATABASE IF NOT EXISTS luxury_case3;
USE luxury_case3;
CREATE TABLE IF NOT EXISTS segments (
  segment_id INT NOT NULL,
  segment VARCHAR(100) NOT NULL,
  reachable_buyers INT NOT NULL,
  wtp_mean INT NOT NULL,
  interest_mean DECIMAL(18,6) NOT NULL,
  PRIMARY KEY (segment_id)
);
CREATE TABLE IF NOT EXISTS strategies (
  strategy_id INT NOT NULL,
  strategy VARCHAR(100) NOT NULL,
  price INT NOT NULL,
  realization DECIMAL(18,6) NOT NULL,
  unit_cogs INT NOT NULL,
  unit_service INT NOT NULL,
  unit_acquisition INT NOT NULL,
  initial_investment INT NOT NULL,
  annual_fixed INT NOT NULL,
  cannibalization_rate DECIMAL(18,6) NOT NULL,
  brand_haircut DECIMAL(18,6) NOT NULL,
  demand_factor DECIMAL(18,6) NOT NULL,
  PRIMARY KEY (strategy_id)
);
CREATE TABLE IF NOT EXISTS scenarios (
  scenario_id INT NOT NULL,
  scenario VARCHAR(100) NOT NULL,
  volume_factor DECIMAL(18,6) NOT NULL,
  cost_factor DECIMAL(18,6) NOT NULL,
  risk_factor DECIMAL(18,6) NOT NULL,
  PRIMARY KEY (scenario_id)
);
CREATE TABLE IF NOT EXISTS years (
  year INT NOT NULL,
  period INT NOT NULL,
  ramp DECIMAL(18,6) NOT NULL,
  PRIMARY KEY (year)
);
CREATE TABLE IF NOT EXISTS assumptions (
  assumption_id INT NOT NULL,
  discount_rate DECIMAL(18,6) NOT NULL,
  conversion_calibration DECIMAL(18,6) NOT NULL,
  mechanical_units INT NOT NULL,
  mechanical_net_price INT NOT NULL,
  mechanical_margin DECIMAL(18,6) NOT NULL,
  max_cannibalization DECIMAL(18,6) NOT NULL,
  max_brand_haircut DECIMAL(18,6) NOT NULL,
  PRIMARY KEY (assumption_id)
);
CREATE TABLE IF NOT EXISTS respondents (
  respondent_id INT NOT NULL,
  segment_id INT NOT NULL,
  max_wtp INT NOT NULL,
  heritage_owner INT NOT NULL,
  preferred_channel VARCHAR(100) NOT NULL,
  PRIMARY KEY (respondent_id),
  FOREIGN KEY (segment_id) REFERENCES segments(segment_id)
);
CREATE TABLE IF NOT EXISTS responses (
  respondent_id INT NOT NULL,
  strategy_id INT NOT NULL,
  interested INT NOT NULL,
  PRIMARY KEY (respondent_id,strategy_id),
  FOREIGN KEY (respondent_id) REFERENCES respondents(respondent_id),
  FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id)
);
