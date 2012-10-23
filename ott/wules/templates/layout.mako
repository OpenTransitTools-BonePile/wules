# -*- coding: utf-8 -*- 
<!DOCTYPE html>  
<html>
<head>
    <meta charset="utf-8">
    <title>TriMet Example - Pylons and Mako</title>
    <meta name="author" content="Mr. TriMet">
    <link rel="shortcut icon" href="/images/favicon.ico">
    <link rel="stylesheet"    href="/css/style.css">
    <link rel="stylesheet"    href="/css/vote.css">
    <script src="/js/analytics.js"></script>
    <script src="http://code.jquery.com/jquery-latest.js"></script>
</head>

<body>
    % if request.session.peek_flash():
    <div id="flash">
        <% flash = request.session.pop_flash() %>
        % for message in flash:
            ${message}<br>
        % endfor
    </div>
    % endif

    <div id="page">

        ${next.body()}

    </div>
    <script>trinet_page_view();</script>
</body>
</html>
