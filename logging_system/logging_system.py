import os
import json

path_to_json_id = os.path.join(os.path.dirname(__file__), "log_id.json")

def WriteLogs(time: str, thread_url: str, judges_mention: list) -> str:
    with open(path_to_json_id, "r") as read_file:
        data = json.loads(read_file.read())
        log_id = data["id"]

    judges_mention_names = ""

    for member in judges_mention:
        judges_mention_names += f"{member.name} : {member.id}\n"
    
    text = (f"Создание нового обжалования, log_id: {log_id}\n"
            f"время: {time}, ссылка на публикацию: {thread_url}\n"
            f"было упомянуто: {len(judges_mention)} судей \n"
            f"список упомянутых судей:\n{judges_mention_names}"
    )
    
    with open(path_to_json_id, "w") as read_file:
        log_id += 1
        data_dict = {"id": log_id}
        data_json = json.dumps(data_dict)
        read_file.write(data_json)
    return text