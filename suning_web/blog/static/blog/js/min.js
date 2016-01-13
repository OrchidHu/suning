window.onload=function(){
var pricee=document.getElementById("price").textContent;
//alert(pricee[0])
var price=eval(pricee)
//alert(price);
var usdeur = [];//这里的月份少了一个月，下面显示的地方都要+1月=
for(var i=price.length-1;i>=0;i--){
    usdeur.push([Date.UTC(price[i][0],price[i][1]-1,price[i][2]),price[i][3]]);
};
//usdeur=[  [Date.UTC(2015,9,20),1],   [Date.UTC(2015,9,24),2], [Date.UTC(2015,9,25),3]  ]
//alert(usdeur);
 $(function () {
	    var data="";
        var chart = new Highcharts.StockChart({
            chart: {
                renderTo: 'container'//指向的div的id属性
            },
            lang:{
                        months: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
                        shortMonths: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一', '十二'],
                        weekdays: ['星期天', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
                    },
            exporting: {
                enabled: false //是否能导出趋势图图片  
            },
            credits:{
            enabled:false
            },
            title: {
         enabled:false
                },
            xAxis : {
				tickPixelInterval: 200,//x轴上的间隔   
            type: 'datetime', //定义x轴上日期的显示格式  
            labels: {  
            formatter: function() {  
                var vDate=new Date(this.value);
				data=vDate.getFullYear()+"-"+(vDate.getMonth()+1)+"-"+vDate.getDate()
                return data;  
            },  
            align: 'center'  
        } 
			},
            yAxis: {

                title: {
                    text: '价格（￥）'  //y轴上的标题  
                }
            },
            gridLineColor:"#eee",
            tooltip: {
            formatter: function() {
				var s = "";
				
				$.each(this.points, function(i, point) {
                var vDate = new Date(point.x);
                vDate=vDate.getFullYear() + "-" +(vDate.getMonth()+1) + "-" + vDate.getDate();
					s += vDate+'<br/>1号店￥<b>'+ point.y +'</b>';
				});
				return s;
                }
            },
            rangeSelector: {
                        buttons: [{
                                type: 'week',
                                count: 1,
                                text: '1周内'
                            },{
                                type: 'month',
                                count: 1,
                                text: '1个月'
                            }, {
                                type: 'month',
                                count: 3,
                                text: '3个月'
                            }, {
                                type: 'all',
                                text: '所有'
                            }],
                        selected:2,
                        buttonSpacing:10,
                        inputEnabled: false
                    },
                    scrollbar: { enabled: true },
            navigator:{enabled:false},
            series: [{
                name: '1号店',  
                data: usdeur,//属性值  
                marker : {  
                      enabled : true,
                      radius : 2  
                  },  
            }]
        });
    });  
};