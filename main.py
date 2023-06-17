from deepface import DeepFace
import json


def face_verify(path_img_1, path_img_2):
    """Функция для сравнения лиц между собой"""
    try:
        normalized_path_1 = path_img_1.replace('"', '').replace('\\', '/')
        normalized_path_2 = path_img_2.replace('"', '').replace('\\', '/')

        result_dict = DeepFace.verify(img1_path=normalized_path_1, img2_path=normalized_path_2, enforce_detection=False)
        result_dict['verified'] = str(result_dict['verified'])

        saved_path = f'face_verify_results/{normalized_path_1[normalized_path_1.rfind("/") + 1:normalized_path_1.rfind(".")]}_{normalized_path_2[normalized_path_2.rfind("/") + 1:normalized_path_2.rfind(".")]}.json'

        with open(saved_path, 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)

        if result_dict['verified'] == 'True':
            return f'Проверка пройдена. Успех! Путь до файла: {saved_path}'
        return f'Проверка провалена. Ошибка! Путь до файла: {saved_path}'

    except Exception as _ex:
        return _ex


def face_recognition(path_img, path_directory):
    """Функция проверки наличия лица в директории"""
    try:
        normalized_path_img = path_img.replace('"', '').replace('\\', '/')
        normalized_path_dir = path_directory.replace('"', '').replace('\\', '/')

        result_dict = DeepFace.find(img_path=normalized_path_img , db_path=normalized_path_dir, enforce_detection=False)[0]['identity'].to_dict()

        saved_path = f'face_recognition_result/{normalized_path_img[normalized_path_img.rfind("/") + 1:normalized_path_img.rfind(".")]}_in_{normalized_path_dir[normalized_path_dir.rfind("/") + 1:]}.json'

        with open(saved_path, 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)

        return result_dict

    except Exception as _ex:
        return _ex


def face_analyze(path_img):
    """Анализ лица на пол, возраст и т.д"""
    try:
        normalized_path_img = path_img.replace('"', '').replace('\\', '/')

        result_dict = DeepFace.analyze(img_path=normalized_path_img, actions=("gender", "age", "emotion", "race"), enforce_detection=False)

        compact_dict = {'Пол': result_dict[0]['dominant_gender'],
                        'Возраст': result_dict[0]['age'],
                        'Эмоция': result_dict[0]['dominant_emotion'],
                        'Раса': result_dict[0]['dominant_race']}

        for key, value in compact_dict.items():
            print(f'{key}: {value}')

        saved_path = f'face_analyze_results/{normalized_path_img[normalized_path_img.rfind("/") + 1:normalized_path_img.rfind(".")]}.json'

        with open(saved_path, 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)

        return f'Процесс завершен! Путь до файла: {saved_path}'

    except Exception as _ex:
        return _ex


def main():
    actions = {1: 'Сравнение лиц между собой', 2: 'Проверка наличия лица в директории', 3: 'Анализ лица'}

    for key, value in actions.items():
        print(f'{key} => {value}')

    desired_action = int(input('Выберите номер желаемого действия: '))

    if desired_action not in actions.keys():
        raise KeyError(f'Действия с номером {desired_action} нет в списке!')

    if desired_action == 1:
        path_img_1 = input('Введите путь до первого изображения: ')
        path_img_2 = input('Введите путь до второго изображения: ')
        print(face_verify(path_img_1, path_img_2))

    elif desired_action == 2:
        path_img = input('Введите путь до изображения: ')
        path_directory = input('Введите путь до директории: ')
        result = face_recognition(path_img, path_directory)
        if len(result) > 0:
            print(f'Найдено {len(result)} похожих!')
            for key, value in result.items():
                print(f'{key + 1}) {value}')
        else:
            print(f'Ничего не найдено!')

    elif desired_action == 3:
        path_img = input('Введите путь до изображения: ')
        print(face_analyze(path_img))


if __name__ == '__main__':
    main()