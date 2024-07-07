import json
import boto3
import os
import subprocess

s3 = boto3.client('s3')

def transcode_step_func_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }
    bucket_name = 'content-bucket-cloud-app-movie2'
    file_key = event.get('movie_id')
    resolution = event.get('resolution')
    folder_path = event.get('S3_FOLDER_PATH')
    # shared_data["movie_id"] = generated_uuid
    # shared_data["resolution"] = resolution
    # shared_data["S3_FOLDER_PATH"] = S3_FOLDER_PATH
    error_message = str(os.listdir('/opt/bin'))
    test = "proba"
    result = ""
    try:
        # Preuzmite metapodatke fajla
        # response = s3.head_object(Bucket=bucket_name, Key="movies/"+file_key)
        #
        # # Izvucite tip sadržaja
        # content_type = response['ContentType']
        #
        # # Mapiranje MIME tipova na ekstenzije
        # mime_to_extension = {
        #     'video/mp4': '.mp4',
        #     # Dodajte druge tipove i ekstenzije ako je potrebno
        # }
        #
        # # Dodelite odgovarajuću ekstenziju
        # file_extension = mime_to_extension.get(content_type, '')
        file_extension = ".mp4"

        # Definišite lokalnu putanju gde će se fajl preuzeti
        local_file_path = f'/tmp/{file_key}{file_extension}'
        # print("ajded:" + local_file_path)
        input_file_path = f'/tmp/{os.path.basename(file_key)}{file_extension}'
        output_file_path = f'/tmp/resized_{test}_{os.path.basename(file_key)}'
        # os.mkdir(output_file_path)
        # os.remove(output_file_path)

        # if os.path.exists(input_file_path):
        #     print(f"Ulazni fajl postoji: {input_file_path}")
        # else:
        #     print(f"Ulazni fajl ne postoji: {input_file_path}")

        # Preuzimanje fajla iz S3
        s3.download_file(bucket_name, folder_path+file_key, input_file_path)



        # if os.path.exists(input_file_path):
        #     print(f"Ulazni fajl postoji: {input_file_path}")
        # else:
        #     print(f"Ulazni fajl ne postoji: {input_file_path}")

        print(os.listdir("/tmp"))
        command = [
            '/opt/bin/ffmpeg', '-y',
            '-i', input_file_path,
            '-vf', f'scale={resolution[0]}:{resolution[1]}',
            '-preset', 'ultrafast', '-crf', '23', '-c:a', 'copy',
            output_file_path+".mp4"
        ]


        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        resized_file_key = f"resized_{resolution}_{os.path.basename(file_key)}"
        s3.upload_file(output_file_path+".mp4", bucket_name, folder_path+resized_file_key,ExtraArgs={'ContentType': 'video/mp4'})


        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Video resized successfully',
                'resizedFileKey': resized_file_key
            }),
            'headers': headers
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error_message': str(e)
            }),
            'headers': headers
        }



