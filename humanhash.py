"""
humanhash: Human-readable representations of digests.

The simplest ways to use this module are the :func:`humanize` and :func:`uuid`
functions. For tighter control over the output, see :class:`HumanHasher`.
"""

import operator
import uuid as uuidlib


DEFAULT_WORDLIST = ('nlp', 'nosql', 'photoshop', 'saas', 'xcode', 'sqlserver', 'hadoop', 'data-scientist', 'mysql', 'ninja', 'openstack', 'visual-studio', 'code-review', 'integrity', 'mobile-app', 'developer', 'xml', 'native-app', 'apache-cordova', 'candidate', 'mumbai', 'analytics', 'flash', 'cdns', 'celery', 'usability', 'equity', 'localizations', 'junit', 'css3', 'activities', 'meteor', 'iit-bombay', 'python', 'evaluate', 'rake', 'postgis', 'psd', 'functional', 'appstore', 'background', 'jenkins', 'web-sockets', 'excellent-negotiating', 'mocha', 'java-script', 'ie9', 'storyboard', 'open-source', 'data-mining', 'make', 'rabbitmq', 'server', 'digital-media', 'scalable-architecture', 'team', 'mapkit', 'security', 'cms', 'rack', 'detailed-job', 'crm', 'front-end', 'javascript-engineers', 'foundation', 'adobe', 'rockstar', 'dilbert', 'android-sdks', 'twitter', 'startup', 'job-requirements', 'iim-calcutta', 'layouts', 'growth', 'design', 'kickass', 'reviewer', 'team-player', 'postgres', 'social-networks', 'expert', 'phonegap', 'android-studio', 'redis', 'angular-js', 'version', 'seo-', 'cakephp', 'full-stack', 'backend', 'jasmin', 'core', 'hibernate', 'java-programming', 'business', 'web', 'internship', 'aws', 'javascript', 'jasmine', 'iconic', 'web-developer', 'tdd', 'ajax', 'china', 'html5', 'ubuntu', 'apache', 'strong', 'graphic-designer', 'laravel', 'pune', 'web-servcies', 'postgresql', 'constraint', 'php-developer', 'industry', 'experience', 'keen', 'joomla', 'mvc', 'elasticsearch', 'adobe-photoshop', 'sass', 'ionic', 'new-delhi', 'vacation-policy', 'apple', 'social-media', 'devops', 'cocoa', 'unix', 'api', 'linux', 'sounds', 'ios-developer', 'engineer', 'iim-bangalore', 'git', 'java', 'codeigniter', 'free', 'software-developer', 'nosql-db', 'perl', 'json', 'wordpress', 'iphone', 'criteria', 'widgets', 'mks', 'lean-practices', 'energy', 'big-data-analytics', 'define', 'function', 'iit', 'newsletters', 'company', 'memory', 'j2ee', 'rspec', 'ec2', 'iit-delhi', 'grunt', 'ruby', 'sdk', 'jquery', 'project-manager', 'analyze', 'illustrator', 'tomcat', 'embedded', 'web-app', 'rest-api', 'work', 'eclipse', 'objective-c', 'senior-architect', 'lead', 'lucene', 'frameworks', 'compensation', 'open-gl', 'stock-options', 'jquery-mobile', 'nashik', 'android-apis', 'restful', 'requirejs', 'user-interface', 'sqlite', 'documentation', 'mongo', 'springmvc', 'big-data', 'india', 'sales', 'linkedin', 'koramangala', 'iit-kanpur', 'ansible', 'expertise', 'angularjs', 'silicon-valley', 'technology', 'html-designer', 'ipad-developer', 'adwords', 'webgl', 'firmware', 'vagrant', 'indiranagar', 'phonegap-developer', 'ceo', 'html', 'esops', 'machine-learning', 'online', 'performance', 'android', 'pandas', 'css', 'karma', 'node', 'gurgaon', 'bonus', 'mongodb', 'senior-ux', 'ios', 'scalability', 'mouth', 'plan', 'sql', 'services', 'tech-lead', 'php', 'data', 'svn', 'paas', 'designers', 'github', 'technical-lead', 'algorithm', 'database', 'url', 'bootstrap', 'san-francisco', 'django', 'client', 'advocacy', 'databases', 'coordinate', 'frontend-developers', 'mac-os')


class HumanHasher(object):

    """
    Transforms hex digests to human-readable strings.

    The format of these strings will look something like:
    `victor-bacon-zulu-lima`. The output is obtained by compressing the input
    digest to a fixed number of bytes, then mapping those bytes to one of 256
    words. A default wordlist is provided, but you can override this if you
    prefer.

    As long as you use the same wordlist, the output will be consistent (i.e.
    the same digest will always render the same representation).
    """

    def __init__(self, wordlist=DEFAULT_WORDLIST):
        if len(wordlist) != 256:
            raise ValueError("Wordlist must have exactly 256 items")
        self.wordlist = wordlist

    def humanize(self, hexdigest, words=4, separator='-'):

        """
        Humanize a given hexadecimal digest.

        Change the number of words output by specifying `words`. Change the
        word separator with `separator`.

            >>> digest = '60ad8d0d871b6095808297'
            >>> HumanHasher().humanize(digest)
            'sodium-magnesium-nineteen-hydrogen'
        """

        # Gets a list of byte values between 0-255.
        bytes = map(lambda x: int(x, 16),
                    map(''.join, zip(hexdigest[::2], hexdigest[1::2])))
        # Compress an arbitrary number of bytes to `words`.
        compressed = self.compress(bytes, words)
        # Map the compressed byte values through the word list.
        return separator.join(self.wordlist[byte] for byte in compressed)

    @staticmethod
    def compress(bytes, target):

        """
        Compress a list of byte values to a fixed target length.

            >>> bytes = [96, 173, 141, 13, 135, 27, 96, 149, 128, 130, 151]
            >>> HumanHasher.compress(bytes, 4)
            [205, 128, 156, 96]

        Attempting to compress a smaller number of bytes to a larger number is
        an error:

            >>> HumanHasher.compress(bytes, 15)  # doctest: +ELLIPSIS
            Traceback (most recent call last):
            ...
            ValueError: Fewer input bytes than requested output
        """

        length = len(bytes)
        if target > length:
            raise ValueError("Fewer input bytes than requested output")

        # Split `bytes` into `target` segments.
        seg_size = length // target
        segments = [bytes[i * seg_size:(i + 1) * seg_size]
                    for i in xrange(target)]
        # Catch any left-over bytes in the last segment.
        segments[-1].extend(bytes[target * seg_size:])

        # Use a simple XOR checksum-like function for compression.
        checksum = lambda bytes: reduce(operator.xor, bytes, 0)
        checksums = map(checksum, segments)
        return checksums

    def uuid(self, **params):

        """
        Generate a UUID with a human-readable representation.

        Returns `(human_repr, full_digest)`. Accepts the same keyword arguments
        as :meth:`humanize` (they'll be passed straight through).
        """

        digest = str(uuidlib.uuid4()).replace('-', '')
        return self.humanize(digest, **params), digest


DEFAULT_HASHER = HumanHasher()
uuid = DEFAULT_HASHER.uuid
humanize = DEFAULT_HASHER.humanize
