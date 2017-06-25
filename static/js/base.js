/**
 * Created by bilixin on 17-3-7.
 */

$(function(){
    $("#btn_login").click(function(){
        datas = {'stu_ID': $("#id_stu_ID").val(), 'password': $("#id_password").val()};
        $.ajax({
          url: "/login/",
          type:"POST",
          data: datas,
          success: function(data) {
              data = eval(data)
              alert(data['result']);
              if (data['result'] == 'success')
                  location.href = '/search-result/';
                  // $.get('/search-result/').attr("target", "_blank")
          },
          error: function(){
                alert("table loading error...");
          }
        });

        })
    });


$(document).on("click", "#select", function(){
    $.cookie("year", $("#id_year").val())
    $.cookie("month", $("#id_month").val())
});



$(function(){
   $(".box input").click(function(){
       alert("123");
   });
})
