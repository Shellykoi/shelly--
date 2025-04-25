from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 模拟已存在的班级数据
existing_classes = ['DD-01', 'CS-101', 'MATH-202']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_class', methods=['POST'])
def add_class():
    data = request.json
    class_id = data.get('class_id', '').strip()
    student_count = data.get('student_count', '').strip()

    # 验证数据
    if not class_id:
        return jsonify({'success': False, 'message': '班号不能为空！'})

    if not student_count:
        return jsonify({'success': False, 'message': '人数不能为空！'})

    if not student_count.isdigit():
        return jsonify({'success': False, 'message': '人数必须为数字！'})

    if class_id in existing_classes:
        return jsonify({'success': False, 'message': f'班级 {class_id} 已存在！'})

    # 模拟添加成功
    existing_classes.append(class_id)
    return jsonify({'success': True, 'message': f'班级 {class_id} 添加成功！'})


if __name__ == '__main__':
    app.run(debug=True)


