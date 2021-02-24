// Copyright 2021 kanzchip-8 Project Authors. Licensed under MIT License.

use std::fs::OpenOptions;
use std::io::prelude::*;

pub const DEBUG: u8 = 0;
pub const INFO: u8 = 1;
pub const WARNING: u8 = 2;
pub const ERROR: u8 = 3;
const LOGFILE: &str = "kanzchip-8.log";

macro_rules! log_debug {
    ($log_message:expr) => {
        // if logger::LogLevel::get_log_level() >= logger::DEBUG {
            let s = format!("DEBUG:[{}:{}]: {}", file!(), line!(), $log_message);
            println!("{}", s);
            logger::log_to_file(&s);    
        // }
    };
}

macro_rules! log_info {
    ($log_message:expr) => {
        // if logger::LogLevel::get_log_level() >= logger::INFO {
            let s = format!("INFO:[{}:{}]: {}", file!(), line!(), $log_message);
            println!("{}", s);
            logger::log_to_file(&s);
        // }
    };
}

macro_rules! log_warning {
    ($log_message:expr) => {
        // if logger::LogLevel::get_log_level() >= logger::WARNING {
            let s = format!("WARNING:[{}:{}]: {}", file!(), line!(), $log_message);
            println!("{}", s);
            logger::log_to_file(&s);
        // }
    };
}

macro_rules! log_error {
    ($log_message:expr) => {
        let s = format!("ERROR:[{}:{}]: {}", file!(), line!(), $log_message);
        println!("{}", s);
        logger::log_to_file(&s);
    };
}

// pub struct LogLevel {
//     level: u8,
// }

// impl LogLevel {
//     pub fn set_log_level(severity: u8) {
//         LogLevel { level: severity };
//     }

//     pub fn get_log_level(&self) -> u8 {
//         return self.level;
//     }
// }


// Should not be used from outside but need to be pub for macros to work.
// Another solution could be to duplicate this code in macros above.
pub fn log_to_file(log_message: &str) {
    let mut file = OpenOptions::new()
        .write(true)
        .create(true)
        .append(true)
        .open(LOGFILE)
        .unwrap();

    if let Err(e) = writeln!(file, "{}", log_message) {
        eprintln!("Couldn't write to file: {}", e);
    }
}

