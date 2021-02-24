// Copyright 2021 kanzchip-8 Project Authors. Licensed under MIT License.

#[macro_use]
mod logger;

fn main() {
    println!("Print hex values! 0x{:0>4X} and 0x{:0>4x}", 10, 512);

    log_error!("HELLO!");
    log_warning!("Hello World");
    log_info!("Hello World...");
    log_debug!("Hello World.....");
}
