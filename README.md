# course_crawler

Crawler able to scrap Coursera's webpage. It creates several csv files with the following information, one for each type of training:

<ol>
  <li> url: url of the course </li>
  <li> name': name of the course (it might not be en English). </li>
  <li> topics' : topics (from the domains in Coursera).  </li>
  <li> skills': related skills from Coursera's skill knowledge graph.  </li>
  <li> type': type of training (it can be 'specialization', 'course', 'mastertrack', 'project' or 'certificate'). </li>
  <li> description': description of the course (it might not be in English. </li>
</ol>

Eventually it will be extended to other platforms (e.g. edX, Udemy...).