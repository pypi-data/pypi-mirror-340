import requests
from collections import deque 
from .util import get_url_domain
from .util import UrlList
import re
import threading
import time

class WebWeaver:
    """
    A web crawler class that provides functionality to crawl websites and extract links.
    This class supports both single-page crawling and complete site mapping with 
    options for multi-threading to improve performance.
    """

    def crawl_url(self, url, timeout=2):
        """
        Crawls a single URL and extracts all href links from the page.
        
        Args:
            url (str): The URL to crawl
            timeout (int): Request timeout in seconds (default: 2)
            
        Returns:
            list: List of extracted URLs, returns [None] if the request fails
            
        Note:
            Uses regex to find href attributes while excluding favicon links and anchors
        """
        try:
            reqs = requests.get(url,timeout=timeout)
        except:
            return [None]
        url_pattern = r'\shref=\"\s*(?!.*favicon)(?!#)([^\'\"<>\s]+)\s*\"'
        matching_tags = re.findall(url_pattern, reqs.text)
        return matching_tags

    def crawl_url_sitemap(self, url, timeout, session, url_list):
        """
        Crawls a single URL using an existing session and updates the URL list.
        
        Args:
            url (str): The URL to crawl
            timeout (int): Request timeout in seconds
            session (requests.Session): Session object for making requests
            url_list (UrlList): Object to track different types of URLs
            
        Returns:
            list: List of extracted URLs, returns [None] if the request fails
            
        Note:
            This method is used internally by crawl_site to maintain session persistence
        """
        try:
            reqs = session.get(url,timeout=timeout)
        except:
            return [None]
        url_list.urls.add(url)
        url_pattern = r'\shref=\"\s*(?!.*favicon)(?!#)([^\'\"<>\s]+)\s*\"'
        matching_tags = re.findall(url_pattern, reqs.text)
        return matching_tags

    def crawl_site(self, urls, timeout = 2, limit = 5):
        """
        Performs a breadth-first crawl of a website starting from given URLs.
        
        Args:
            urls (list): List of starting URLs to crawl
            timeout (int): Request timeout in seconds (default: 2)
            limit (int): Maximum number of pages to crawl (default: 5)
            
        Returns:
            UrlList: Object containing sets of normal, abnormal, and error URLs
            
        Note:
            - Uses a queue for breadth-first traversal
            - Handles relative and absolute URLs
            - Maintains a session for connection pooling
        """
        q = deque()
        url_list = UrlList()
        session = requests.Session()
        for url in urls:
            q.append(url)
        count_urls_crawlled = 0
        
        while(q and count_urls_crawlled<=limit):
            url = q.popleft()
            count_urls_crawlled+=1
            extracted_urls = self.crawl_url_sitemap(url, timeout, session,url_list)
            domain_name = get_url_domain(url)
            
            # Handle failed requests
            if len(extracted_urls)!=0 and extracted_urls[0]==None:
                url_list.error_urls.add(url)
                continue
                
            # Process extracted URLs
            for extracted_url_i in extracted_urls:
                extracted_url = extracted_url_i
                if extracted_url==None:
                    continue
                    
                # Clean and normalize URLs
                extracted_url = extracted_url.strip()
                if(extracted_url[:4]!="http"):
                    url_list.abnormal_urls.add(extracted_url)
                    if extracted_url[0]!='/':
                        extracted_url = '/' + extracted_url
                    extracted_url = domain_name + extracted_url
                extracted_url.rstrip('/')
                
                # Add new URLs to queue if not already processed
                if((extracted_url not in url_list.urls) and (extracted_url not in url_list.error_urls)):
                    q.append(extracted_url)
                    url_list.urls.add(extracted_url)
        session.close()
        return url_list

    def crawl_url_sitemap_multiThreading(self, url, timeout, session, url_list,q):
        """
        Multi-threaded version of URL crawling for improved performance.
        
        Args:
            url (str): The URL to crawl
            timeout (int): Request timeout in seconds
            session (requests.Session): Session object for making requests
            url_list (UrlList): Object to track different types of URLs
            q (deque): Queue for managing URLs to be crawled
            
        Note:
            - Thread-safe implementation for parallel crawling
            - Shares session and URL list objects across threads
        """
        try:
            reqs = session.get(url,timeout=timeout)
        except:
            url_list.error_urls.add(url)
            return 
        url_list.urls.add(url)
        url_pattern = r'\shref=\"\s*(?!.*favicon)(?!#)([^\'\"<>\s]+)\s*\"'
        #url_pattern = r'\shref=\"\s*(?!#)(?!.*(favicon|\.pdf|\.jpg|\.png|\.gif|\.css|\.js|\.ico|\.svg|utm_|sort=|page=|order=|logout|wp-admin|admin|profile|delete-account))([^\'\"<>\s]+)\s*\"'
        extracted_urls = re.findall(url_pattern, reqs.text)
        
        domain_name = get_url_domain(url)
        for extracted_url_i in extracted_urls:
            extracted_url = extracted_url_i
            if extracted_url==None:
                continue
                
            # Process and normalize URLs
            extracted_url = extracted_url.strip()
            if(extracted_url[:4]!="http"):
                url_list.abnormal_urls.add(extracted_url)
                if extracted_url[0]!='/':
                    extracted_url = '/' + extracted_url
                extracted_url = domain_name + extracted_url
            extracted_url.rstrip('/')
            
            # Add new URLs to queue if not already processed
            if((extracted_url not in url_list.urls) and (extracted_url not in url_list.error_urls)):
                q.append(extracted_url)
                url_list.urls.add(extracted_url)

    def crawl_site_multiThreading(self, urls, timeout = 2, limit = 5, no_of_threads = 16):
        """
        Performs a multi-threaded crawl of a website for improved performance.
        
        Args:
            urls (list): List of starting URLs to crawl
            timeout (int): Request timeout in seconds (default: 2)
            limit (int): Maximum number of pages to crawl (default: 5)
            no_of_threads (int): Number of concurrent threads to use (default: 16)
            
        Returns:
            UrlList: Object containing sets of normal, abnormal, and error URLs
            
        Note:
            - Creates multiple threads to crawl URLs concurrently
            - Uses thread synchronization to manage shared resources
            - Maintains a session for connection pooling
        """
        q = deque()
        url_list = UrlList()
        session = requests.Session()
        for url in urls:
            q.append(url)
        count_urls_crawlled = 0
        
        while(q and count_urls_crawlled<=limit):
            threads = []
            # Create and start threads
            for _ in range(no_of_threads):
                if not q or count_urls_crawlled>limit:
                    break
                url = q.popleft()
                count_urls_crawlled+=1
                thread = threading.Thread(target=self.crawl_url_sitemap_multiThreading, 
                                       args=(url, timeout, session,url_list,q))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            #extracted_urls = self.crawl_url_sitemap(url, timeout, session,url_list)
            
        session.close()
        return url_list



