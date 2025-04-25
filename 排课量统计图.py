import random
import json
from jinja2 import Template

# 教育艺术学院的教师名单（减少到35位）
teachers = [
    "程双儿", "巩俞含", "曹立汶", "王艺璇", "薄媛元",
    "李雪瑶", "常阳", "马逸伦", "赵银芳", "靳忠宏",
    "董家佑", "刘星", "高占鹏", "罗梦娇", "史正兵",
    "赵兰兰", "唐阳阳", "刘玉阁", "刘亚萍", "赵雪宁",
    "李富丽", "高艺祯", "于东晖", "石云", "赵伟华",
    "李杰超", "张萍", "陈娟霞", "王凡兰", "孙思邈",
    "曹镛", "郭娜", "马华丽", "罗薇", "向晓琼"
]

# 为每个教师生成随机排课量
teacher_data = [{'姓名': teacher, '排课量': random.randint(1, 8)} for teacher in teachers]

# 使用你提供的配色方案
color_scheme = ["#e4e4e4", "#d5deef", "#b2caee", "#89afe0", "#3a5985"]

# 学院信息
colleges = [
    "教育艺术学院", "化学与材料工程学院", "信息智能工程学院",
    "公共基础学院", "马克思主义学院", "汽车与智能交通学院",
    "机械电气工程学院", "现代农业学院", "教务处", "党委行政办公室"
]

# 生成HTML模板
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>教育艺术学院教师排课量看板</title>
    <script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.4.1/echarts.min.js"></script>
    <style>
        body { 
            padding: 20px; 
            font-family: Arial; 
            background-color: #f0f2f5; 
        }
        .chart-container { 
            width: 1200px; 
            height: 650px; /* 调整高度以减少空白 */
            margin: 0 auto; 
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
            padding: 20px; 
            position: relative; 
        }
        .select-box {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 10;
            padding: 5px;
            font-size: 14px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: white;
        }
        #chart { 
            width: 100%; 
            height: 75%; /* 调整图表高度 */
        }
        .week-line {
            width: 90%;
            height: 50px;
            margin: 10px auto 0; /* 调整上边距，离图表更近 */
            position: relative;
            border-bottom: 2px solid #3a5985;
        }
        .week-line::after {
            content: '➤';
            position: absolute;
            right: -20px;
            bottom: -10px;
            font-size: 20px;
            color: #3a5985;
        }
        .week-dot {
            position: absolute;
            bottom: -5px;
            width: 10px;
            height: 10px;
            background: #3a5985;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s;
        }
        .week-dot.active {
            width: 15px;
            height: 15px;
            background: #89afe0;
        }
        .week-label {
            position: absolute;
            bottom: -25px;
            font-size: 12px;
            color: #3a5985;
        }
        .week-info {
            position: absolute;
            top: 10px;
            left: 20px;
            font-size: 14px;
            color: #3a5985;
        }
    </style>
</head>
<body>
    <div class="chart-container">
        <select class="select-box" id="collegeSelect">
            {% for college in colleges %}
            <option value="{{ college }}">{{ college }}</option>
            {% endfor %}
        </select>
        <div id="chart"></div>
        <div class="week-line" id="weekLine">
            <!-- 周一到周日的圆点和标签 -->
            <div class="week-dot" style="left: 0%;" data-week="周一"></div>
            <div class="week-label" style="left: 0%;">周一</div>
            <div class="week-dot" style="left: 16.66%;" data-week="周二"></div>
            <div class="week-label" style="left: 16.66%;">周二</div>
            <div class="week-dot" style="left: 33.33%;" data-week="周三"></div>
            <div class="week-label" style="left: 33.33%;">周三</div>
            <div class="week-dot" style="left: 50%;" data-week="周四"></div>
            <div class="week-label" style="left: 50%;">周四</div>
            <div class="week-dot" style="left: 66.66%;" data-week="周五"></div>
            <div class="week-label" style="left: 66.66%;">周五</div>
            <div class="week-dot" style="left: 83.33%;" data-week="周六"></div>
            <div class="week-label" style="left: 83.33%;">周六</div>
            <div class="week-dot" style="left: 100%;" data-week="周日"></div>
            <div class="week-label" style="left: 100%;">周日</div>
        </div>
        <div class="week-info" id="weekInfo">当前周：<span id="selectedWeek">周一</span></div>
    </div>

    <script>
        var teacherData = {{ teacher_data_json }};
        var colorScheme = {{ color_scheme_json }};
        var chartDom = document.getElementById('chart');
        var myChart = echarts.init(chartDom, 'light');

        // 提取教师姓名和排课量
        var teachers = teacherData.map(t => t['姓名']);
        var courses = teacherData.map(t => t['排课量']);

        // 配置图表
        var option = {
            title: { 
                text: '教育艺术学院教师排课量', 
                left: 'center', 
                textStyle: { 
                    fontSize: 16, 
                    fontWeight: 'normal' // 标题不加粗
                } 
            },
            tooltip: { trigger: 'axis' },
            xAxis: {
                type: 'category',
                data: teachers,
                axisLabel: { rotate: 45 }
            },
            yAxis: { 
                type: 'value',
                name: '节数',
                max: 8
            },
            series: [{
                data: courses,
                type: 'bar',
                itemStyle: { 
                    color: function(params) {
                        return colorScheme[params.dataIndex % colorScheme.length];
                    }
                },
                barWidth: '60%'
            }],
            grid: { bottom: '20%' }
        };

        // 渲染图表
        myChart.setOption(option);

        // 下拉框事件监听（示例功能）
        var select = document.getElementById('collegeSelect');
        select.addEventListener('change', function() {
            alert('你选择了：' + this.value); // 这里可以扩展为动态加载其他学院数据
        });

        // 周圆点点击事件
        var weekDots = document.querySelectorAll('.week-dot');
        var weekInfo = document.getElementById('weekInfo');
        var selectedWeek = document.getElementById('selectedWeek');

        weekDots.forEach(dot => {
            dot.addEventListener('click', function() {
                // 移除所有圆点的 active 类
                weekDots.forEach(d => d.classList.remove('active'));
                // 为当前圆点添加 active 类
                this.classList.add('active');
                // 更新选中的周信息
                selectedWeek.textContent = this.getAttribute('data-week');
            });
        });

        // 默认选中周一
        weekDots[0].click();
    </script>
</body>
</html>
'''

# 渲染模板并生成HTML
template = Template(html_template)
html_output = template.render(
    teacher_data_json=json.dumps(teacher_data, ensure_ascii=False),
    color_scheme_json=json.dumps(color_scheme, ensure_ascii=False),
    colleges=colleges
)

with open('edu_art_schedule.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("文件已生成：edu_art_schedule.html")