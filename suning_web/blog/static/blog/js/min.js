window.onload=function(){
var pricee=document.getElementById("price").textContent;
//alert(pricee[0])
var price=eval(pricee)
//alert(price);
var usdeur = [];//������·�����һ���£�������ʾ�ĵط���Ҫ+1��=
for(var i=price.length-1;i>=0;i--){
    usdeur.push([Date.UTC(price[i][0],price[i][1]-1,price[i][2]),price[i][3]]);
};
//usdeur=[  [Date.UTC(2015,9,20),1],   [Date.UTC(2015,9,24),2], [Date.UTC(2015,9,25),3]  ]
//alert(usdeur);
 $(function () {
	    var data="";
        var chart = new Highcharts.StockChart({
            chart: {
                renderTo: 'container'//ָ���div��id����
            },
            lang:{
                        months: ['һ��', '����', '����', '����', '����', '����', '����', '����', '����', 'ʮ��', 'ʮһ��', 'ʮ����'],
                        shortMonths: ['һ��', '����', '����', '����', '����', '����', '����', '����', '����', 'ʮ��', 'ʮһ', 'ʮ��'],
                        weekdays: ['������', '����һ', '���ڶ�', '������', '������', '������', '������']
                    },
            exporting: {
                enabled: false //�Ƿ��ܵ�������ͼͼƬ  
            },
            credits:{
            enabled:false
            },
            title: {
         enabled:false
                },
            xAxis : {
				tickPixelInterval: 200,//x���ϵļ��   
            type: 'datetime', //����x�������ڵ���ʾ��ʽ  
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
                    text: '�۸񣨣���'  //y���ϵı���  
                }
            },
            gridLineColor:"#eee",
            tooltip: {
            formatter: function() {
				var s = "";
				
				$.each(this.points, function(i, point) {
                var vDate = new Date(point.x);
                vDate=vDate.getFullYear() + "-" +(vDate.getMonth()+1) + "-" + vDate.getDate();
					s += vDate+'<br/>1�ŵ꣤<b>'+ point.y +'</b>';
				});
				return s;
                }
            },
            rangeSelector: {
                        buttons: [{
                                type: 'week',
                                count: 1,
                                text: '1����'
                            },{
                                type: 'month',
                                count: 1,
                                text: '1����'
                            }, {
                                type: 'month',
                                count: 3,
                                text: '3����'
                            }, {
                                type: 'all',
                                text: '����'
                            }],
                        selected:2,
                        buttonSpacing:10,
                        inputEnabled: false
                    },
                    scrollbar: { enabled: true },
            navigator:{enabled:false},
            series: [{
                name: '1�ŵ�',  
                data: usdeur,//����ֵ  
                marker : {  
                      enabled : true,
                      radius : 2  
                  },  
            }]
        });
    });  
};