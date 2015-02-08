# Release Notes

## [0.2.0]

- ...

## [0.1.0]

[Under Development]

- initial release with core functionality working

[0.2.0]: https://github.com/pythonindia/junction/issues?q=milestone%3A%22release+0.2.0%22
[0.1.0]: https://github.com/pythonindia/junction/issues?q=milestone%3A%22release+0.1.0+-+initial+release%22

<!-- autolinks #12 to an github issue -->
<script src="https://padolsey.github.io/findAndReplaceDOMText/src/findAndReplaceDOMText.js"></script>
<script>
    var repo = 'pythonindia/junction';
    findAndReplaceDOMText(document.querySelector('[role="main"]'), {
      find: /#(\d+)/g,
      replace: function(portion, match){
        var el = document.createElement("a");
        el.setAttribute('href', 'http://github.com/'+ repo +'/issues/'+ match[1]);
        el.setAttribute('target', '_blank');
        el.innerHTML = portion.text;
        return el;
        }
    });
</script>
