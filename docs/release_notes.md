# Release Notes

## [0.4.0][0.4.0]

- Fix filters on the proposal review form #418 (@ChillarAnand)
- Update proposal urls to use hashids. The slug will now update itself when the title of proposal changes.
- Conference duration is displayed in a short form.
- Add ability to remove a casted vote on a proposal.
- ...

## [0.3.0][0.3.0]

__Date:__ 31st March 2016

__Features__

- conference moderators can be added per conference using a `conference_moderator` management command.
- Improved conference admin.
- Basic REST API for accessing conference details and proposals.
- REST API to submit feedback for a talk/workshop.
- UI updates  

__Fixes__
-  fix the tag filtering for all the proposal sections inside proposal list (#170)
- Update proposal detail styling (#207)


## [0.2.0][0.2.0]

__Date:__ 29th March 2015

__Added__
- add support for fig based development environment (#129)
- django admin got a new theme based on django-flat-theme
- setup social sharing on proposal detail pages (#185)
- add `SITE_URL` settings to support path based root url of site. 
- add docker/fig setup
- add celery support
- send mail to reviewers for new proposals

__Changes__
- hide reviewer name in comments (#193)
- UI: remove 'description' from page proposals list (#149)
- update styling of create proposal forms

__Fixes__
- upgrade django and other libraries to latest
- fix incorrect login url on comment section

## [0.1.0]

__Date:__ 8th February 2015

- initial release with core functionality working

[0.4.0]: https://github.com/pythonindia/junction/compare/0.3.0...master
[0.3.0]: https://github.com/pythonindia/junction/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/pythonindia/junction/compare/0.1.0...0.2.0
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
