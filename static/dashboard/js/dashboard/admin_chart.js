

(function($) {
    /* "use strict" */

 var dlabChartlist = function(){

	var screenWidth = $(window).width();


	var pieChart3 = function(data){
		 var options = {
          series: data,
          chart: {
          type: 'donut',
		  height:230
        },
		dataLabels:{
			enabled: false
		},
		stroke: {
          width: 0,
        },
		colors:['#F6AD2E', 'var(--primary)', '#412EFF', '#fc03fc'],
		legend: {
              position: 'bottom',
			  show:false
            },
        responsive: [{
          breakpoint: 768,
          options: {
           chart: {
			  height:200
			},
          }
        }]
        };

        var chart = new ApexCharts(document.querySelector("#AdminChart"), options);
        chart.render();

	}

	const getChartStat=()=>{
			fetch('/super_admin/stat_skill_admin').then((res)=>res.json().then((results)=>{
				const category_stat = results.final_stat;
				const [labels, data] = [Object.keys(category_stat), Object.values(category_stat)];
				pieChart3(data);
			}));
	};
	getChartStat();



	/* Function ============ */
		return {
			init:function(){
			},


			load:function(){
				pieChart3();

			},

			resize:function(){
			}
		}

	}();



	jQuery(window).on('load',function(){
		setTimeout(function(){
			dlabChartlist.load();
		}, 1000);

	});



})(jQuery);