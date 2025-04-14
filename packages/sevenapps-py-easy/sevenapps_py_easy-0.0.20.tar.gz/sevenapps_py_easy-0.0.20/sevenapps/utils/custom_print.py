def custom_print(tag='', message='', type='manual'):
    if type == 'manual':
            print(f'[{tag}] {message}')
    elif type == 'debug':
        print(f'[DEBUG] {message}')
    elif type == 'empty_line':
        print('')
    elif type == 'info':
        print(f'[INFO] {message}')
    elif type == 'error':
        print(f'\033[91m[ERROR] {message}\033[0m')
    elif type == 'success':
        print(f'\033[92m[SUCCESS] {message}\033[0m')
    elif type == 'warning':
        print(f'\033[93m[WARNING] {message}\033[0m')
    elif type == 'html':
        print(f'<pre><code>{message}</code></pre>')
    elif type == 'json':
        print(json.dumps(json.loads(message), indent=4))
    elif type == 'bold':
        print(f'\033[1m{message}\033[0m')
    elif type == 'italic':
        print(f'\033[3m{message}\033[0m')
    elif type == 'underline':
        print(f'\033[4m{message}\033[0m')
    else:
        print(f'{message}')

