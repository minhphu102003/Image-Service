from kafka_library.consumer import consume_messages

if __name__ == "__main__":
    topic = "extrac_image" 
    group_id = "groud_extract"  

    consume_messages(topic, group_id)