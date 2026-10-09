// Marks not-yet-released music as such in the visitor's browser, so the
// site doesn't need a rebuild when a release date passes. Without JS the
// markup stays in its "already released" state.
(function () {
    var now = Date.now();
    document.querySelectorAll('[data-release-date]').forEach(function (el) {
        var release = Date.parse(el.getAttribute('data-release-date'));
        if (isNaN(release) || release <= now) {
            return;
        }
        el.classList.add('is-unreleased');
        var days = Math.ceil((release - now) / 86400000);
        el.querySelectorAll('.music-preview-date').forEach(function (date) {
            date.textContent += ' (' + days + (days === 1 ? ' day' : ' days') + ' left)';
        });
        el.querySelectorAll('[data-presave]').forEach(function (presave) {
            presave.hidden = false;
        });
    });
})();
