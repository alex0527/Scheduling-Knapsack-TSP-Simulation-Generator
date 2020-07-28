

def create():
    table_create = {}

    table_create['users'] = """
        CREATE TABLE users (
         `user_id` VARCHAR(255) NOT NULL,
         `password` VARCHAR(255) NOT NULL,
         `first_name` VARCHAR(255) NOT NULL,
         `last_name` VARCHAR(255) NOT NULL,
         `email_address` VARCHAR(255) NOT NULL,
         `phone_number` VARCHAR(13) NOT NULL,
         `address` VARCHAR(255) NOT NULL,
         PRIMARY KEY (`user_id`)
         ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """

    table_create['tracking'] = """
        CREATE TABLE tracking (
             `tracking_id` VARCHAR(255) NOT NULL,
             `status` VARCHAR(255) NOT NULL,
             `created_at` VARCHAR(255) NOT NULL,
             `estimated_delivered_at` VARCHAR(255) NOT NULL,
             `delay` BOOLEAN NOT NULL,
             `previous_destination` VARCHAR(255) NOT NULL,
             `previous_destination_start_time` VARCHAR(255) NOT NULL,
             PRIMARY KEY (`tracking_id`)
         ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """

    table_create['station'] = """
        CREATE TABLE station (
             `station_id` INT NOT NULL,
             `drone_num` INT NOT NULL,
             `robot_num` INT NOT NULL,
             `address` VARCHAR(1025) NOT NULL,
             `lon` DOUBLE NOT NULL,
             `lat` DOUBLE NOT NULL,
             PRIMARY KEY (`station_id`)
         ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """

    table_create['machine'] = """
        CREATE TABLE machine (
             `machine_id` INT NOT NULL,
             `station_id` INT NOT NULL,
             `machine_type` VARCHAR(255) NOT NULL,
             `available` BOOLEAN NOT NULL,
             `height_limit` FLOAT NOT NULL,
             `weight_limit` FLOAT NOT NULL,
             `unit_price_per_mile_per_kg` FLOAT NOT NULL,
             PRIMARY KEY (`machine_id`),
             FOREIGN KEY (`station_id`) REFERENCES `station` (`station_id`)
         ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """

    table_create['contact'] = """
        CREATE TABLE contact (
             `contact_id` INT NOT NULL AUTO_INCREMENT,
             `first_name` VARCHAR(255) NOT NULL,
             `last_name` VARCHAR(255) NOT NULL,
             `phone_number` VARCHAR(20) NOT NULL,
             `email_address` VARCHAR(255) NOT NULL,
             `address` VARCHAR(1025),
             PRIMARY KEY (`contact_id`)
         ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """

    table_create['orders'] = """
        CREATE TABLE orders (
            `order_id` VARCHAR(255) NOT NULL,
            `user_id` VARCHAR(255) NOT NULL,
            `tracking_id` VARCHAR(255) NOT NULL,
            `station_id` INT NOT NULL,
            `machine_id` INT,
            `active` BOOLEAN NOT NULL,
            `sender_id` INT NOT NULL,
            `recipient_id` INT NOT NULL,
            `package_weight` FLOAT NOT NULL,
            `package_height` FLOAT NOT NULL,
            `package_fragile` BOOLEAN NOT NULL,
            `package_length` FLOAT NOT NULL,
            `package_width` FLOAT NOT NULL,
            `carrier` VARCHAR(255) NOT NULL,
            `total_cost` FLOAT NOT NULL,
            `appointment_time` VARCHAR(45) NOT NULL,
            PRIMARY KEY (`order_id`),
            FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
            FOREIGN KEY (`tracking_id`) REFERENCES `tracking` (`tracking_id`),
            FOREIGN KEY (`station_id`) REFERENCES `station` (`station_id`),
            FOREIGN KEY (`machine_id`) REFERENCES `machine` (`machine_id`),
            FOREIGN KEY (`sender_id`) REFERENCES `contact` (`contact_id`),
            FOREIGN KEY (`recipient_id`) REFERENCES `contact` (`contact_id`)
         ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """
    return table_create

