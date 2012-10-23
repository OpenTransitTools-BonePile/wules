# -*- coding: utf-8 -*- 

<script>
function submit_vote(value, stopid, userid)
{
    console.log(value, stopid, userid);
    $.post("/vote", { user_id: userid, stop_id: stopid, vote_value: value } );
}
</script>

<fieldset class="rating">
    <legend>Please rate stop id #${pageargs['stop_id']}:</legend>
    % for item in ("Palace", "Good", "Meh", "Bad", "Al M Special"):
        <input type="radio" id="star${loop.reverse_index + 1}" name="rating" value="${loop.reverse_index + 1}" 
            onclick="submit_vote(this.value, ${pageargs['stop_id']}, ${pageargs['user_id']})"
            xonclick="${request.route_url('vote', user_id=(loop.reverse_index + 1), stop_id='xx', vote_value='xx') }"
            xonclick="${request.route_url('vote') }"
            %if pageargs['current_vote'] == (loop.reverse_index + 1):
            checked="checked"
            %endif
        />
        <label for="star${loop.reverse_index + 1}" title="${item}">&nbsp; ${loop.reverse_index  + 1} star</label>
    % endfor
</fieldset>