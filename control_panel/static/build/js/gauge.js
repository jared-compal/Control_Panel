


console.log('init_gauge [' + $('.gauge-chart').length + ']');

console.log('init_gauge');


var chart_gauge_settings = {
  lines: 12,
  angle: 0,
  lineWidth: 0.4,
  pointer: {
	  length: 0.75,
	  strokeWidth: 0.042,
	  color: '#1D212A'
  },
  limitMax: 'false',
  colorStart: '#007fff',
  colorStop: '#007fff',
  strokeColor: '#d0d0d0',
  generateGradient: true
};

if ($('#chart_gauge_01').length){
	var chart_gauge_01_elem = document.getElementById('chart_gauge_01');
	var chart_gauge_01 = new Gauge(chart_gauge_01_elem).setOptions(chart_gauge_settings);
}
if ($('#gauge-text').length){
	chart_gauge_01.maxValue = 1000;
	chart_gauge_01.animationSpeed = 17;
	chart_gauge_01.set(650);
	chart_gauge_01.setTextField(document.getElementById("gauge-text"));
}
if ($('#chart_gauge_02').length){
	var chart_gauge_02_elem = document.getElementById('chart_gauge_02');
	var chart_gauge_02 = new Gauge(chart_gauge_02_elem).setOptions(chart_gauge_settings);
}
if ($('#gauge-text2').length){
	chart_gauge_02.maxValue = 1000;
	chart_gauge_02.animationSpeed = 17;
	chart_gauge_02.set(210);
	chart_gauge_02.setTextField(document.getElementById("gauge-text2"));
}

var i;
for (i in data) {
	console.log(i);
	var gauge_name = 'chart_gauge_0' + i;
	if ($('#' + gauge_name).length){
	var gauge_name_elem = document.getElementById(gauge_name);
	var gauge_name = new Gauge(gauge_name_elem).setOptions(chart_gauge_settings);
	}
	if ($('#gauge-text' + i).length){
		gauge_name.maxValue = data[i][3][1];
		gauge_name.animationSpeed = 17;
		gauge_name.set(data[i][3][0]);
		gauge_name.setTextField(document.getElementById("gauge-text" + i));
	}
}

