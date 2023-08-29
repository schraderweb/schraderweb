
            /* chart.js chart examples */

// chart colors
var colors = ['#007bff','#28a745','#444444','#c3e6cb','#dc3545','#6c757d'];

var chBar = document.getElementById("chBar");
var chartData = {
  labels: ["1", "2", "3", "4", "5", "6", "7", "8"],
  datasets: [{
    data: [445, 483, 503, 689, 692, 634, 503, 689],
    backgroundColor: colors[0]
  }]
//  {
//    data: [209, 245, 383, 403, 589, 692, 580],
//    backgroundColor: colors[1]
//  },
//  {
//    data: [489, 135, 483, 290, 189, 603, 600],
//    backgroundColor: colors[2]
//  },
//  {
//    data: [639, 465, 493, 478, 589, 632, 674],
//    backgroundColor: colors[4]
//  }]
};

if (chBar) {
  new Chart(chBar, {
  type: 'bar',
  data: chartData,
  options: {
    scales: {
      xAxes: [{
        barPercentage: 0.5,
        categoryPercentage: 0.5
      }],
      yAxes: [{
        ticks: {
          beginAtZero: false,
          display: false
        }
      }]
    },
    legend: {
      display: false
    }
  }
  });
}
            
        
            /* chart.js chart examples */

// chart colors
var colors = ['#007bff','#28a745','#444444','#c3e6cb','#dc3545','#6c757d'];

var chBar = document.getElementById("chBar1");
var chartData = {
  labels: ["1", "2", "3", "4", "5", "6"],
  datasets: [{
    data: [445, 483, 503, 689, 692, 634],
    backgroundColor: colors[0]
  }]
//  {
//    data: [209, 245, 383, 403, 589, 692, 580],
//    backgroundColor: colors[1]
//  },
//  {
//    data: [489, 135, 483, 290, 189, 603, 600],
//    backgroundColor: colors[2]
//  },
//  {
//    data: [639, 465, 493, 478, 589, 632, 674],
//    backgroundColor: colors[4]
//  }]
};

if (chBar) {
  new Chart(chBar, {
  type: 'bar',
  data: chartData,
  options: {
    scales: {
      xAxes: [{
        barPercentage: 0.4,
        categoryPercentage: 0.5
      }],
      yAxes: [{
        ticks: {
          beginAtZero: false,
         display: false
        }
      }]
    },
    legend: {
      display: false
    }
  }
  });
}
            
        
              $('body').on('mouseenter mouseleave','.dropdown-hover',function(e){
     let dropdown=$(e.target).closest('.dropdown-hover');
      dropdown.addClass('show');
      
    setTimeout(function(){
          dropdown[dropdown.is(':hover')?'addClass':'removeClass']('show');
      },300);
  });
        
        
        
        $(document).ready(function() {

    
    var readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.profile-pic').attr('src', e.target.result);
            }
    
            reader.readAsDataURL(input.files[0]);
        }
    }
    

    $(".file-upload").on('change', function(){
        readURL(this);
    });
    
    $(".upload-button").on('click', function() {
       $(".file-upload").click();
    });
});