// reverse root-level comments
$(document).ready(function(){
    ul = $('ul.comment-root');
    ul.children().each(function(i,li){ul.prepend(li)});
    ul.css("visibility", "visible");
});

// toggle reply form
$(document).ready(function(){
    $(".comment-reply").bind("click", function(e){
        e.preventDefault();
        $(".comment-form-reply").hide();
        $(this).parent().siblings(".comment-form-reply").show();
    });

    $(".button-hide-form").bind("click.a", function(e){
        e.preventDefault();
        $(this).parent().hide();
    });
});