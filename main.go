package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"
)

// SpiderConfig holds configuration for the web spider
type SpiderConfig struct {
	MaxDepth    int
	MaxPages    int
	Delay       time.Duration
	UserAgent   string
	Timeout     time.Duration
	Concurrency int
}

// NewSpiderConfig creates a new spider configuration with defaults
func NewSpiderConfig() *SpiderConfig {
	return &SpiderConfig{
		MaxDepth:    3,
		MaxPages:    100,
		Delay:       time.Second,
		UserAgent:   "DirectWebSpider/1.0",
		Timeout:     30 * time.Second,
		Concurrency: 5,
	}
}

// SetMaxDepth sets the maximum crawl depth
func (c *SpiderConfig) SetMaxDepth(depth int) error {
	if depth < 0 {
		return fmt.Errorf("max depth cannot be negative")
	}
	c.MaxDepth = depth
	return nil
}

// SetMaxPages sets the maximum number of pages to crawl
func (c *SpiderConfig) SetMaxPages(pages int) error {
	if pages < 0 {
		return fmt.Errorf("max pages cannot be negative")
	}
	c.MaxPages = pages
	return nil
}

// SetDelay sets the delay between requests
func (c *SpiderConfig) SetDelay(delay time.Duration) error {
	if delay < 0 {
		return fmt.Errorf("delay cannot be negative")
	}
	c.Delay = delay
	return nil
}

// SetUserAgent sets the user agent string
func (c *SpiderConfig) SetUserAgent(ua string) error {
	if ua == "" {
		return fmt.Errorf("user agent cannot be empty")
	}
	c.UserAgent = ua
	return nil
}

// SetTimeout sets the request timeout
func (c *SpiderConfig) SetTimeout(timeout time.Duration) error {
	if timeout <= 0 {
		return fmt.Errorf("timeout must be positive")
	}
	c.Timeout = timeout
	return nil
}

// SetConcurrency sets the number of concurrent workers
func (c *SpiderConfig) SetConcurrency(concurrency int) error {
	if concurrency < 1 {
		return fmt.Errorf("concurrency must be at least 1")
	}
	c.Concurrency = concurrency
	return nil
}

// Validate validates the spider configuration
func (c *SpiderConfig) Validate() error {
	if c.MaxDepth < 0 {
		return fmt.Errorf("invalid max depth: %d", c.MaxDepth)
	}
	if c.MaxPages < 0 {
		return fmt.Errorf("invalid max pages: %d", c.MaxPages)
	}
	if c.Delay < 0 {
		return fmt.Errorf("invalid delay: %v", c.Delay)
	}
	if c.UserAgent == "" {
		return fmt.Errorf("user agent cannot be empty")
	}
	if c.Timeout <= 0 {
		return fmt.Errorf("invalid timeout: %v", c.Timeout)
	}
	if c.Concurrency < 1 {
		return fmt.Errorf("invalid concurrency: %d", c.Concurrency)
	}
	return nil
}

// Spider represents a web spider
type Spider struct {
	config *SpiderConfig
	client *http.Client
	logger *log.Logger
}

// NewSpider creates a new spider instance
func NewSpider(config *SpiderConfig) (*Spider, error) {
	if config == nil {
		return nil, fmt.Errorf("config cannot be nil")
	}
	
	if err := config.Validate(); err != nil {
		return nil, fmt.Errorf("invalid config: %w", err)
	}
	
	client := &http.Client{
		Timeout: config.Timeout,
	}
	
	logger := log.New(os.Stdout, "[SPIDER] ", log.LstdFlags)
	
	return &Spider{
		config: config,
		client: client,
		logger: logger,
	}, nil
}

// Crawl starts crawling from the given URL
func (s *Spider) Crawl(url string) error {
	if url == "" {
		return fmt.Errorf("URL cannot be empty")
	}
	
	s.logger.Printf("Starting crawl from: %s", url)
	
	// Simulate crawling process
	for i := 0; i < s.config.MaxPages; i++ {
		select {
		case <-time.After(s.config.Delay):
			s.logger.Printf("Crawling page %d/%d", i+1, s.config.MaxPages)
			
			// Simulate HTTP request
			resp, err := s.client.Get(url)
			if err != nil {
				s.logger.Printf("Error fetching %s: %v", url, err)
				continue
			}
			resp.Body.Close()
			
			s.logger.Printf("Successfully crawled page %d", i+1)
		}
	}
	
	s.logger.Printf("Crawl completed")
	return nil
}

// CrawlWithCallback crawls with a callback function
func (s *Spider) CrawlWithCallback(url string, callback func(string, error)) error {
	if url == "" {
		return fmt.Errorf("URL cannot be empty")
	}
	
	if callback == nil {
		return fmt.Errorf("callback cannot be nil")
	}
	
	s.logger.Printf("Starting crawl with callback from: %s", url)
	
	for i := 0; i < s.config.MaxPages; i++ {
		select {
		case <-time.After(s.config.Delay):
			// Simulate processing
			pageURL := fmt.Sprintf("%s/page%d", url, i+1)
			callback(pageURL, nil)
		}
	}
	
	return nil
}

// GetStats returns spider statistics
func (s *Spider) GetStats() map[string]interface{} {
	return map[string]interface{}{
		"max_depth":    s.config.MaxDepth,
		"max_pages":    s.config.MaxPages,
		"delay":        s.config.Delay.String(),
		"user_agent":   s.config.UserAgent,
		"timeout":      s.config.Timeout.String(),
		"concurrency":  s.config.Concurrency,
	}
}

// Close closes the spider and cleans up resources
func (s *Spider) Close() error {
	s.logger.Printf("Closing spider")
	// Cleanup logic would go here
	return nil
}

// Utility functions

// IsValidURL checks if a URL is valid
func IsValidURL(url string) bool {
	if url == "" {
		return false
	}
	// Simple URL validation
	return len(url) > 7 && (url[:7] == "http://" || url[:8] == "https://")
}

// ExtractDomain extracts domain from URL
func ExtractDomain(url string) (string, error) {
	if !IsValidURL(url) {
		return "", fmt.Errorf("invalid URL: %s", url)
	}
	
	// Simple domain extraction
	if len(url) > 7 && url[:7] == "http://" {
		url = url[7:]
	} else if len(url) > 8 && url[:8] == "https://" {
		url = url[8:]
	}
	
	// Find first slash
	if slashIndex := len(url); slashIndex > 0 {
		for i, char := range url {
			if char == '/' {
				slashIndex = i
				break
			}
		}
		url = url[:slashIndex]
	}
	
	return url, nil
}

// ParseDelay parses delay from string
func ParseDelay(delayStr string) (time.Duration, error) {
	if delayStr == "" {
		return 0, fmt.Errorf("delay string cannot be empty")
	}
	
	// Try parsing as duration
	duration, err := time.ParseDuration(delayStr)
	if err != nil {
		// Try parsing as seconds
		seconds, err := strconv.Atoi(delayStr)
		if err != nil {
			return 0, fmt.Errorf("invalid delay format: %s", delayStr)
		}
		duration = time.Duration(seconds) * time.Second
	}
	
	if duration < 0 {
		return 0, fmt.Errorf("delay cannot be negative")
	}
	
	return duration, nil
}

// ProcessURL processes a URL and returns processed data
func ProcessURL(url string) (map[string]interface{}, error) {
	if !IsValidURL(url) {
		return nil, fmt.Errorf("invalid URL: %s", url)
	}
	
	domain, err := ExtractDomain(url)
	if err != nil {
		return nil, fmt.Errorf("failed to extract domain: %w", err)
	}
	
	return map[string]interface{}{
		"url":    url,
		"domain": domain,
		"valid":  true,
		"time":   time.Now().Unix(),
	}, nil
}

// BatchProcessURLs processes multiple URLs in batch
func BatchProcessURLs(urls []string) ([]map[string]interface{}, error) {
	if len(urls) == 0 {
		return nil, fmt.Errorf("URLs list cannot be empty")
	}
	
	results := make([]map[string]interface{}, 0, len(urls))
	
	for i, url := range urls {
		result, err := ProcessURL(url)
		if err != nil {
			return nil, fmt.Errorf("failed to process URL %d (%s): %w", i, url, err)
		}
		results = append(results, result)
	}
	
	return results, nil
}

// Error types
type SpiderError struct {
	Type    string
	Message string
	URL     string
}

func (e *SpiderError) Error() string {
	return fmt.Sprintf("%s: %s (URL: %s)", e.Type, e.Message, e.URL)
}

// NewSpiderError creates a new spider error
func NewSpiderError(errorType, message, url string) *SpiderError {
	return &SpiderError{
		Type:    errorType,
		Message: message,
		URL:     url,
	}
}

// Constants
const (
	DefaultMaxDepth    = 3
	DefaultMaxPages    = 100
	DefaultDelay       = time.Second
	DefaultUserAgent   = "DirectWebSpider/1.0"
	DefaultTimeout     = 30 * time.Second
	DefaultConcurrency = 5
)

// Version information
var (
	Version   = "1.0.0"
	BuildTime = "unknown"
	GitCommit = "unknown"
)

// GetVersion returns version information
func GetVersion() map[string]string {
	return map[string]string{
		"version":    Version,
		"build_time": BuildTime,
		"git_commit": GitCommit,
	}
}

// main function
func main() {
	fmt.Println("Direct Web Spider - Go Backend")
	fmt.Printf("Version: %s\n", Version)
	
	// Create default config
	config := NewSpiderConfig()
	
	// Create spider
	spider, err := NewSpider(config)
	if err != nil {
		log.Fatalf("Failed to create spider: %v", err)
	}
	defer spider.Close()
	
	// Print stats
	stats := spider.GetStats()
	fmt.Printf("Spider Stats: %+v\n", stats)
	
	// Print version info
	version := GetVersion()
	fmt.Printf("Version Info: %+v\n", version)
	
	// Test utility functions
	testURL := "https://example.com"
	if IsValidURL(testURL) {
		domain, err := ExtractDomain(testURL)
		if err != nil {
			log.Printf("Failed to extract domain: %v", err)
		} else {
			fmt.Printf("Domain: %s\n", domain)
		}
	}
	
	// Test URL processing
	result, err := ProcessURL(testURL)
	if err != nil {
		log.Printf("Failed to process URL: %v", err)
	} else {
		fmt.Printf("Processed URL: %+v\n", result)
	}
	
	// Test batch processing
	urls := []string{"https://example.com", "https://google.com"}
	results, err := BatchProcessURLs(urls)
	if err != nil {
		log.Printf("Failed to batch process URLs: %v", err)
	} else {
		fmt.Printf("Batch processed %d URLs\n", len(results))
	}
}
