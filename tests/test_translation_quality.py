#!/usr/bin/env python3
"""
Translation Quality Assessment - Real-World Code Patterns

Tests semantic preservation and code quality across all 25 language combinations.
Goes beyond "does it generate something" to "does it generate CORRECT, COMPILABLE code".

Quality Metrics:
- Compilation validity (would it compile/run?)
- Semantic preservation (same behavior?)
- Idiomatic code (language conventions?)
- Type accuracy (specific types vs generic?)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2

from language.python_generator_v2 import generate_python
from language.nodejs_generator_v2 import generate_nodejs
from language.go_generator_v2 import generate_go
from language.rust_generator_v2 import generate_rust
from language.dotnet_generator_v2 import generate_csharp

from dsl.ir import IRModule
from typing import Dict, List, Tuple, Any


# ============================================================================
# Real-World Test Code Patterns
# ============================================================================

REAL_WORLD_PATTERNS = {
    "async_http_request": {
        "Python": '''
import asyncio
import aiohttp
from typing import Dict, Any

async def fetch_user_data(user_id: int) -> Dict[str, Any]:
    """Fetch user data from API"""
    url = f"https://api.example.com/users/{user_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"API error: {response.status}")
            return await response.json()

async def get_multiple_users(user_ids: list) -> list:
    """Fetch multiple users concurrently"""
    tasks = [fetch_user_data(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)
''',
        "JavaScript": '''
async function fetchUserData(userId) {
    const url = `https://api.example.com/users/${userId}`;
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
}

async function getMultipleUsers(userIds) {
    const promises = userIds.map(uid => fetchUserData(uid));
    return await Promise.all(promises);
}
''',
        "Go": '''
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

func FetchUserData(userId int) (map[string]interface{}, error) {
    url := fmt.Sprintf("https://api.example.com/users/%d", userId)

    resp, err := http.Get(url)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    if resp.StatusCode != 200 {
        return nil, fmt.Errorf("API error: %d", resp.StatusCode)
    }

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }

    var result map[string]interface{}
    err = json.Unmarshal(body, &result)
    return result, err
}
''',
        "Rust": '''
use serde_json::Value;
use std::error::Error;

async fn fetch_user_data(user_id: i32) -> Result<Value, Box<dyn Error>> {
    let url = format!("https://api.example.com/users/{}", user_id);

    let response = reqwest::get(&url).await?;

    if !response.status().is_success() {
        return Err(format!("API error: {}", response.status()).into());
    }

    let data = response.json().await?;
    Ok(data)
}
''',
        "C#": '''
using System;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

public class UserService
{
    private static readonly HttpClient client = new HttpClient();

    public static async Task<JsonDocument> FetchUserData(int userId)
    {
        string url = $"https://api.example.com/users/{userId}";

        HttpResponseMessage response = await client.GetAsync(url);

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"API error: {response.StatusCode}");
        }

        string content = await response.Content.ReadAsStringAsync();
        return JsonDocument.Parse(content);
    }
}
''',
    },

    "error_handling": {
        "Python": '''
from typing import Optional

def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers with error handling"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def safe_divide(a: float, b: float) -> Optional[float]:
    """Safe division that returns None on error"""
    try:
        return divide_numbers(a, b)
    except ValueError as e:
        print(f"Error: {e}")
        return None
''',
        "JavaScript": '''
function divideNumbers(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b;
}

function safeDivide(a, b) {
    try {
        return divideNumbers(a, b);
    } catch (error) {
        console.log(`Error: ${error.message}`);
        return null;
    }
}
''',
        "Go": '''
package main

import (
    "errors"
    "fmt"
)

func DivideNumbers(a float64, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("Cannot divide by zero")
    }
    return a / b, nil
}

func SafeDivide(a float64, b float64) (float64, bool) {
    result, err := DivideNumbers(a, b)
    if err != nil {
        fmt.Printf("Error: %v\\n", err)
        return 0, false
    }
    return result, true
}
''',
        "Rust": '''
use std::error::Error;

fn divide_numbers(a: f64, b: f64) -> Result<f64, Box<dyn Error>> {
    if b == 0.0 {
        return Err("Cannot divide by zero".into());
    }
    Ok(a / b)
}

fn safe_divide(a: f64, b: f64) -> Option<f64> {
    match divide_numbers(a, b) {
        Ok(result) => Some(result),
        Err(e) => {
            println!("Error: {}", e);
            None
        }
    }
}
''',
        "C#": '''
using System;

public class MathOperations
{
    public static double DivideNumbers(double a, double b)
    {
        if (b == 0)
        {
            throw new DivideByZeroException("Cannot divide by zero");
        }
        return a / b;
    }

    public static double? SafeDivide(double a, double b)
    {
        try
        {
            return DivideNumbers(a, b);
        }
        catch (Exception e)
        {
            Console.WriteLine($"Error: {e.Message}");
            return null;
        }
    }
}
''',
    },

    "collections_operations": {
        "Python": '''
from typing import List, Dict

def filter_even_numbers(numbers: List[int]) -> List[int]:
    """Filter even numbers from list"""
    return [n for n in numbers if n % 2 == 0]

def map_to_squares(numbers: List[int]) -> List[int]:
    """Map numbers to their squares"""
    return [n * n for n in numbers]

def group_by_length(words: List[str]) -> Dict[int, List[str]]:
    """Group words by their length"""
    result = {}
    for word in words:
        length = len(word)
        if length not in result:
            result[length] = []
        result[length].append(word)
    return result
''',
        "JavaScript": '''
function filterEvenNumbers(numbers) {
    return numbers.filter(n => n % 2 === 0);
}

function mapToSquares(numbers) {
    return numbers.map(n => n * n);
}

function groupByLength(words) {
    const result = {};
    for (const word of words) {
        const length = word.length;
        if (!result[length]) {
            result[length] = [];
        }
        result[length].push(word);
    }
    return result;
}
''',
        "Go": '''
package main

func FilterEvenNumbers(numbers []int) []int {
    result := make([]int, 0)
    for _, n := range numbers {
        if n % 2 == 0 {
            result = append(result, n)
        }
    }
    return result
}

func MapToSquares(numbers []int) []int {
    result := make([]int, len(numbers))
    for i, n := range numbers {
        result[i] = n * n
    }
    return result
}

func GroupByLength(words []string) map[int][]string {
    result := make(map[int][]string)
    for _, word := range words {
        length := len(word)
        result[length] = append(result[length], word)
    }
    return result
}
''',
        "Rust": '''
use std::collections::HashMap;

pub fn filter_even_numbers(numbers: Vec<i32>) -> Vec<i32> {
    numbers.into_iter()
        .filter(|n| n % 2 == 0)
        .collect()
}

pub fn map_to_squares(numbers: Vec<i32>) -> Vec<i32> {
    numbers.into_iter()
        .map(|n| n * n)
        .collect()
}

pub fn group_by_length(words: Vec<String>) -> HashMap<usize, Vec<String>> {
    let mut result = HashMap::new();
    for word in words {
        let length = word.len();
        result.entry(length).or_insert_with(Vec::new).push(word);
    }
    result
}
''',
        "C#": '''
using System;
using System.Collections.Generic;
using System.Linq;

public class CollectionOperations
{
    public static List<int> FilterEvenNumbers(List<int> numbers)
    {
        return numbers.Where(n => n % 2 == 0).ToList();
    }

    public static List<int> MapToSquares(List<int> numbers)
    {
        return numbers.Select(n => n * n).ToList();
    }

    public static Dictionary<int, List<string>> GroupByLength(List<string> words)
    {
        return words.GroupBy(w => w.Length)
            .ToDictionary(g => g.Key, g => g.ToList());
    }
}
''',
    },

    "class_with_methods": {
        "Python": '''
from typing import List

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total = 0.0

    def add_item(self, name: str, price: float, quantity: int) -> None:
        """Add item to cart"""
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })
        self.total += price * quantity

    def remove_item(self, name: str) -> bool:
        """Remove item from cart by name"""
        for i, item in enumerate(self.items):
            if item["name"] == name:
                self.total -= item["price"] * item["quantity"]
                self.items.pop(i)
                return True
        return False

    def get_total(self) -> float:
        """Get total cart value"""
        return self.total
''',
        "JavaScript": '''
class ShoppingCart {
    constructor() {
        this.items = [];
        this.total = 0.0;
    }

    addItem(name, price, quantity) {
        this.items.push({
            name: name,
            price: price,
            quantity: quantity
        });
        this.total += price * quantity;
    }

    removeItem(name) {
        for (let i = 0; i < this.items.length; i++) {
            if (this.items[i].name === name) {
                this.total -= this.items[i].price * this.items[i].quantity;
                this.items.splice(i, 1);
                return true;
            }
        }
        return false;
    }

    getTotal() {
        return this.total;
    }
}
''',
        "Go": '''
package main

type CartItem struct {
    Name     string
    Price    float64
    Quantity int
}

type ShoppingCart struct {
    Items []CartItem
    Total float64
}

func NewShoppingCart() *ShoppingCart {
    return &ShoppingCart{
        Items: make([]CartItem, 0),
        Total: 0.0,
    }
}

func (c *ShoppingCart) AddItem(name string, price float64, quantity int) {
    item := CartItem{
        Name:     name,
        Price:    price,
        Quantity: quantity,
    }
    c.Items = append(c.Items, item)
    c.Total += price * float64(quantity)
}

func (c *ShoppingCart) RemoveItem(name string) bool {
    for i, item := range c.Items {
        if item.Name == name {
            c.Total -= item.Price * float64(item.Quantity)
            c.Items = append(c.Items[:i], c.Items[i+1:]...)
            return true
        }
    }
    return false
}

func (c *ShoppingCart) GetTotal() float64 {
    return c.Total
}
''',
        "Rust": '''
#[derive(Debug, Clone)]
pub struct CartItem {
    pub name: String,
    pub price: f64,
    pub quantity: i32,
}

#[derive(Debug)]
pub struct ShoppingCart {
    pub items: Vec<CartItem>,
    pub total: f64,
}

impl ShoppingCart {
    pub fn new() -> Self {
        ShoppingCart {
            items: Vec::new(),
            total: 0.0,
        }
    }

    pub fn add_item(&mut self, name: String, price: f64, quantity: i32) {
        let item = CartItem {
            name,
            price,
            quantity,
        };
        self.total += price * quantity as f64;
        self.items.push(item);
    }

    pub fn remove_item(&mut self, name: &str) -> bool {
        if let Some(pos) = self.items.iter().position(|item| item.name == name) {
            let item = &self.items[pos];
            self.total -= item.price * item.quantity as f64;
            self.items.remove(pos);
            true
        } else {
            false
        }
    }

    pub fn get_total(&self) -> f64 {
        self.total
    }
}
''',
        "C#": '''
using System;
using System.Collections.Generic;
using System.Linq;

public class CartItem
{
    public string Name { get; set; }
    public double Price { get; set; }
    public int Quantity { get; set; }
}

public class ShoppingCart
{
    private List<CartItem> items;
    private double total;

    public ShoppingCart()
    {
        items = new List<CartItem>();
        total = 0.0;
    }

    public void AddItem(string name, double price, int quantity)
    {
        items.Add(new CartItem
        {
            Name = name,
            Price = price,
            Quantity = quantity
        });
        total += price * quantity;
    }

    public bool RemoveItem(string name)
    {
        CartItem item = items.FirstOrDefault(i => i.Name == name);
        if (item != null)
        {
            total -= item.Price * item.Quantity;
            items.Remove(item);
            return true;
        }
        return false;
    }

    public double GetTotal()
    {
        return total;
    }
}
''',
    },

    "control_flow": {
        "Python": '''
def find_max(numbers: list) -> int:
    """Find maximum number in list"""
    if not numbers:
        return 0

    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def categorize_age(age: int) -> str:
    """Categorize person by age"""
    if age < 13:
        return "child"
    elif age < 20:
        return "teenager"
    elif age < 65:
        return "adult"
    else:
        return "senior"
''',
        "JavaScript": '''
function findMax(numbers) {
    if (numbers.length === 0) {
        return 0;
    }

    let maxVal = numbers[0];
    for (const num of numbers) {
        if (num > maxVal) {
            maxVal = num;
        }
    }
    return maxVal;
}

function categorizeAge(age) {
    if (age < 13) {
        return "child";
    } else if (age < 20) {
        return "teenager";
    } else if (age < 65) {
        return "adult";
    } else {
        return "senior";
    }
}
''',
        "Go": '''
package main

func FindMax(numbers []int) int {
    if len(numbers) == 0 {
        return 0
    }

    maxVal := numbers[0]
    for _, num := range numbers {
        if num > maxVal {
            maxVal = num
        }
    }
    return maxVal
}

func CategorizeAge(age int) string {
    if age < 13 {
        return "child"
    } else if age < 20 {
        return "teenager"
    } else if age < 65 {
        return "adult"
    } else {
        return "senior"
    }
}
''',
        "Rust": '''
pub fn find_max(numbers: &[i32]) -> i32 {
    if numbers.is_empty() {
        return 0;
    }

    let mut max_val = numbers[0];
    for &num in numbers {
        if num > max_val {
            max_val = num;
        }
    }
    max_val
}

pub fn categorize_age(age: i32) -> &'static str {
    if age < 13 {
        "child"
    } else if age < 20 {
        "teenager"
    } else if age < 65 {
        "adult"
    } else {
        "senior"
    }
}
''',
        "C#": '''
using System;
using System.Linq;

public class Utils
{
    public static int FindMax(int[] numbers)
    {
        if (numbers.Length == 0)
        {
            return 0;
        }

        int maxVal = numbers[0];
        foreach (int num in numbers)
        {
            if (num > maxVal)
            {
                maxVal = num;
            }
        }
        return maxVal;
    }

    public static string CategorizeAge(int age)
    {
        if (age < 13)
        {
            return "child";
        }
        else if (age < 20)
        {
            return "teenager";
        }
        else if (age < 65)
        {
            return "adult";
        }
        else
        {
            return "senior";
        }
    }
}
''',
    },

    "string_operations": {
        "Python": '''
def format_user_info(name: str, age: int, city: str) -> str:
    """Format user information as string"""
    return f"{name} is {age} years old and lives in {city}"

def parse_csv_line(line: str) -> list:
    """Parse CSV line into fields"""
    return [field.strip() for field in line.split(",")]

def is_valid_email(email: str) -> bool:
    """Check if email is valid"""
    return "@" in email and "." in email.split("@")[1]
''',
        "JavaScript": '''
function formatUserInfo(name, age, city) {
    return `${name} is ${age} years old and lives in ${city}`;
}

function parseCsvLine(line) {
    return line.split(",").map(field => field.trim());
}

function isValidEmail(email) {
    const parts = email.split("@");
    return parts.length === 2 && parts[1].includes(".");
}
''',
        "Go": '''
package main

import (
    "fmt"
    "strings"
)

func FormatUserInfo(name string, age int, city string) string {
    return fmt.Sprintf("%s is %d years old and lives in %s", name, age, city)
}

func ParseCsvLine(line string) []string {
    fields := strings.Split(line, ",")
    result := make([]string, len(fields))
    for i, field := range fields {
        result[i] = strings.TrimSpace(field)
    }
    return result
}

func IsValidEmail(email string) bool {
    parts := strings.Split(email, "@")
    if len(parts) != 2 {
        return false
    }
    return strings.Contains(parts[1], ".")
}
''',
        "Rust": '''
pub fn format_user_info(name: &str, age: i32, city: &str) -> String {
    format!("{} is {} years old and lives in {}", name, age, city)
}

pub fn parse_csv_line(line: &str) -> Vec<String> {
    line.split(',')
        .map(|s| s.trim().to_string())
        .collect()
}

pub fn is_valid_email(email: &str) -> bool {
    let parts: Vec<&str> = email.split('@').collect();
    parts.len() == 2 && parts[1].contains('.')
}
''',
        "C#": '''
using System;
using System.Linq;

public class StringOperations
{
    public static string FormatUserInfo(string name, int age, string city)
    {
        return $"{name} is {age} years old and lives in {city}";
    }

    public static string[] ParseCsvLine(string line)
    {
        return line.Split(',').Select(s => s.Trim()).ToArray();
    }

    public static bool IsValidEmail(string email)
    {
        string[] parts = email.Split('@');
        return parts.Length == 2 && parts[1].Contains(".");
    }
}
''',
    },

    "type_annotations": {
        "Python": '''
from typing import Optional, Union, List, Dict

def get_user_by_id(user_id: int) -> Optional[Dict[str, Union[str, int]]]:
    """Get user by ID, return None if not found"""
    if user_id < 0:
        return None
    return {
        "id": user_id,
        "name": "Alice",
        "age": 30
    }

def process_items(items: List[int]) -> int:
    """Calculate sum of items"""
    total = 0
    for item in items:
        total += item
    return total
''',
        "JavaScript": '''
function getUserById(userId) {
    if (userId < 0) {
        return null;
    }
    return {
        id: userId,
        name: "Alice",
        age: 30
    };
}

function processItems(items) {
    let total = 0;
    for (const item of items) {
        total += item;
    }
    return total;
}
''',
        "Go": '''
package main

func GetUserById(userId int) map[string]interface{} {
    if userId < 0 {
        return nil
    }
    return map[string]interface{}{
        "id":   userId,
        "name": "Alice",
        "age":  30,
    }
}

func ProcessItems(items []int) int {
    total := 0
    for _, item := range items {
        total += item
    }
    return total
}
''',
        "Rust": '''
use std::collections::HashMap;

pub fn get_user_by_id(user_id: i32) -> Option<HashMap<String, String>> {
    if user_id < 0 {
        return None;
    }
    let mut user = HashMap::new();
    user.insert("id".to_string(), user_id.to_string());
    user.insert("name".to_string(), "Alice".to_string());
    user.insert("age".to_string(), "30".to_string());
    Some(user)
}

pub fn process_items(items: &[i32]) -> i32 {
    let mut total = 0;
    for &item in items {
        total += item;
    }
    total
}
''',
        "C#": '''
using System;
using System.Collections.Generic;

public class DataProcessor
{
    public static Dictionary<string, object> GetUserById(int userId)
    {
        if (userId < 0)
        {
            return null;
        }
        return new Dictionary<string, object>
        {
            { "id", userId },
            { "name", "Alice" },
            { "age", 30 }
        };
    }

    public static int ProcessItems(List<int> items)
    {
        int total = 0;
        foreach (int item in items)
        {
            total += item;
        }
        return total;
    }
}
''',
    },

    "function_calls": {
        "Python": '''
def calculate_tax(amount: float, rate: float) -> float:
    """Calculate tax amount"""
    return amount * rate

def calculate_total(subtotal: float, tax_rate: float) -> float:
    """Calculate total with tax"""
    tax = calculate_tax(subtotal, tax_rate)
    return subtotal + tax

def format_price(amount: float) -> str:
    """Format price as currency"""
    return f"${amount:.2f}"
''',
        "JavaScript": '''
function calculateTax(amount, rate) {
    return amount * rate;
}

function calculateTotal(subtotal, taxRate) {
    const tax = calculateTax(subtotal, taxRate);
    return subtotal + tax;
}

function formatPrice(amount) {
    return `$${amount.toFixed(2)}`;
}
''',
        "Go": '''
package main

import "fmt"

func CalculateTax(amount float64, rate float64) float64 {
    return amount * rate
}

func CalculateTotal(subtotal float64, taxRate float64) float64 {
    tax := CalculateTax(subtotal, taxRate)
    return subtotal + tax
}

func FormatPrice(amount float64) string {
    return fmt.Sprintf("$%.2f", amount)
}
''',
        "Rust": '''
pub fn calculate_tax(amount: f64, rate: f64) -> f64 {
    amount * rate
}

pub fn calculate_total(subtotal: f64, tax_rate: f64) -> f64 {
    let tax = calculate_tax(subtotal, tax_rate);
    subtotal + tax
}

pub fn format_price(amount: f64) -> String {
    format!("${:.2}", amount)
}
''',
        "C#": '''
using System;

public class PriceCalculator
{
    public static double CalculateTax(double amount, double rate)
    {
        return amount * rate;
    }

    public static double CalculateTotal(double subtotal, double taxRate)
    {
        double tax = CalculateTax(subtotal, taxRate);
        return subtotal + tax;
    }

    public static string FormatPrice(double amount)
    {
        return $"${amount:F2}";
    }
}
''',
    },
}


# ============================================================================
# Quality Assessment Engine
# ============================================================================

class QualityMetric:
    """Represents a quality measurement for translated code."""

    def __init__(self, name: str, score: float, max_score: float, issues: List[str]):
        self.name = name
        self.score = score
        self.max_score = max_score
        self.issues = issues
        self.percentage = (score / max_score * 100) if max_score > 0 else 0

    def __str__(self):
        return f"{self.name}: {self.score}/{self.max_score} ({self.percentage:.1f}%)"


class QualityAssessor:
    """Assess quality of translated code."""

    def assess_compilation_validity(self, code: str, target_lang: str) -> QualityMetric:
        """Check if code would compile/run (syntactic validity)."""
        issues = []
        score = 10.0

        # Basic syntax checks
        if not code or len(code.strip()) == 0:
            issues.append("Empty code generated")
            return QualityMetric("Compilation", 0, 10, issues)

        # Language-specific checks
        if target_lang == "Python":
            if "def " not in code and "class " not in code:
                issues.append("No functions or classes defined")
                score -= 5
            if "    " not in code and "def " in code:
                issues.append("Missing indentation")
                score -= 3
            if code.count("(") != code.count(")"):
                issues.append("Unbalanced parentheses")
                score -= 2

        elif target_lang in ["JavaScript", "TypeScript"]:
            if "function " not in code and "class " not in code and "const " not in code:
                issues.append("No functions or variables defined")
                score -= 5
            if code.count("{") != code.count("}"):
                issues.append("Unbalanced braces")
                score -= 3
            if code.count("(") != code.count(")"):
                issues.append("Unbalanced parentheses")
                score -= 2

        elif target_lang == "Go":
            if "func " not in code and "type " not in code:
                issues.append("No functions or types defined")
                score -= 5
            if "package " not in code:
                issues.append("Missing package declaration")
                score -= 2
            if code.count("{") != code.count("}"):
                issues.append("Unbalanced braces")
                score -= 3

        elif target_lang == "Rust":
            if "fn " not in code and "impl " not in code:
                issues.append("No functions or implementations")
                score -= 5
            if code.count("{") != code.count("}"):
                issues.append("Unbalanced braces")
                score -= 3

        elif target_lang == "C#":
            if "class " not in code and "struct " not in code:
                issues.append("No classes or structs defined")
                score -= 5
            if code.count("{") != code.count("}"):
                issues.append("Unbalanced braces")
                score -= 3

        return QualityMetric("Compilation", max(0, score), 10, issues)

    def assess_semantic_preservation(self, ir_source: IRModule, ir_target: IRModule,
                                   source_lang: str, target_lang: str) -> QualityMetric:
        """Check if semantic meaning is preserved."""
        issues = []
        score = 10.0

        # Function count preservation
        source_func_count = len(ir_source.functions)
        target_func_count = len(ir_target.functions)

        if target_func_count < source_func_count:
            lost = source_func_count - target_func_count
            issues.append(f"Lost {lost} function(s) in translation")
            score -= min(5, lost * 2)

        # Class count preservation
        source_class_count = len(ir_source.classes)
        target_class_count = len(ir_target.classes)

        if target_class_count < source_class_count:
            lost = source_class_count - target_class_count
            issues.append(f"Lost {lost} class(es) in translation")
            score -= min(3, lost * 1.5)

        # Function name preservation (case-insensitive)
        source_names = {f.name.lower() for f in ir_source.functions}
        target_names = {f.name.lower() for f in ir_target.functions}

        missing_names = source_names - target_names
        if missing_names:
            issues.append(f"Missing functions: {', '.join(list(missing_names)[:3])}")
            score -= min(2, len(missing_names))

        return QualityMetric("Semantics", max(0, score), 10, issues)

    def assess_idiomatic_code(self, code: str, target_lang: str) -> QualityMetric:
        """Check if code follows language conventions."""
        issues = []
        score = 10.0

        if target_lang == "Python":
            # PEP 8 checks
            if "def " in code:
                # Check snake_case function names
                import re
                functions = re.findall(r'def (\w+)\(', code)
                for func in functions:
                    if func[0].isupper():
                        issues.append(f"Non-PEP8 function name: {func} (should be snake_case)")
                        score -= 1

            # Check for proper indentation (4 spaces)
            lines = code.split('\n')
            for line in lines:
                if line.startswith(' ') and not line.startswith('    '):
                    indent_count = len(line) - len(line.lstrip())
                    if indent_count % 4 != 0:
                        issues.append("Non-standard indentation (should be 4 spaces)")
                        score -= 1
                        break

        elif target_lang in ["JavaScript", "TypeScript"]:
            # Check camelCase
            import re
            functions = re.findall(r'function (\w+)\(', code)
            for func in functions:
                if '_' in func:
                    issues.append(f"Non-JS function name: {func} (should be camelCase)")
                    score -= 1

            # Check for const/let (not var)
            if "var " in code:
                issues.append("Using 'var' instead of 'const'/'let'")
                score -= 1

        elif target_lang == "Go":
            # Check PascalCase for exported functions
            import re
            functions = re.findall(r'func (\w+)\(', code)
            for func in functions:
                if func[0].islower() and not func.startswith('_'):
                    # Private function, OK
                    pass
                elif func[0].isupper():
                    # Exported, check PascalCase
                    if '_' in func:
                        issues.append(f"Non-Go function name: {func} (should be PascalCase)")
                        score -= 1

            # Check tab indentation
            if '\t' not in code and '    ' in code:
                issues.append("Using spaces instead of tabs")
                score -= 1

        elif target_lang == "Rust":
            # Check snake_case
            import re
            functions = re.findall(r'fn (\w+)\(', code)
            for func in functions:
                if func[0].isupper():
                    issues.append(f"Non-Rust function name: {func} (should be snake_case)")
                    score -= 1

        elif target_lang == "C#":
            # Check PascalCase
            import re
            methods = re.findall(r'public \w+ (\w+)\(', code)
            for method in methods:
                if method[0].islower():
                    issues.append(f"Non-C# method name: {method} (should be PascalCase)")
                    score -= 1

        return QualityMetric("Idioms", max(0, score), 10, issues)

    def assess_type_accuracy(self, ir: IRModule) -> QualityMetric:
        """Check type specificity vs generic fallbacks."""
        issues = []
        score = 10.0

        total_types = 0
        generic_types = 0

        # Check function return types
        for func in ir.functions:
            if func.return_type:
                total_types += 1
                if func.return_type.name in ["any", "object", "interface{}", "unknown"]:
                    generic_types += 1

        # Check function parameter types
        for func in ir.functions:
            for param in func.parameters:
                if param.param_type:
                    total_types += 1
                    if param.param_type.name in ["any", "object", "interface{}", "unknown"]:
                        generic_types += 1

        if total_types > 0:
            generic_percentage = (generic_types / total_types) * 100

            if generic_percentage > 50:
                issues.append(f"{generic_percentage:.1f}% generic types (should be <50%)")
                score -= 5
            elif generic_percentage > 30:
                issues.append(f"{generic_percentage:.1f}% generic types (acceptable but could improve)")
                score -= 2

            # Specific type bonus
            specific_types = total_types - generic_types
            if specific_types == total_types:
                score = 10  # Perfect score

        return QualityMetric("Types", max(0, score), 10, issues)


# ============================================================================
# Matrix Test Runner
# ============================================================================

class QualityMatrixTester:
    """Test quality across all 25 language combinations."""

    def __init__(self):
        self.parsers = {
            "Python": PythonParserV2(),
            "JavaScript": NodeJSParserV2(),
            "Go": GoParserV2(),
            "Rust": RustParserV2(),
            "C#": DotNetParserV2(),
        }

        self.generators = {
            "Python": generate_python,
            "JavaScript": lambda ir: generate_nodejs(ir, typescript=False),
            "TypeScript": lambda ir: generate_nodejs(ir, typescript=True),
            "Go": generate_go,
            "Rust": generate_rust,
            "C#": generate_csharp,
        }

        self.assessor = QualityAssessor()
        self.results = {}

    def test_pattern(self, pattern_name: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """Test one pattern translation."""
        pattern = REAL_WORLD_PATTERNS.get(pattern_name, {})
        source_code = pattern.get(source_lang)

        if not source_code:
            return {
                "success": False,
                "error": f"No test code for {source_lang}",
                "quality_score": 0,
            }

        try:
            # Parse source
            parser = self.parsers[source_lang]
            ir_source = parser.parse_source(source_code, "test")

            if not ir_source or (len(ir_source.functions) == 0 and len(ir_source.classes) == 0):
                return {
                    "success": False,
                    "error": "Failed to parse source code",
                    "quality_score": 0,
                }

            # Generate target
            generator = self.generators[target_lang]
            generated_code = generator(ir_source)

            if not generated_code:
                return {
                    "success": False,
                    "error": "Failed to generate target code",
                    "quality_score": 0,
                }

            # Parse generated code back
            target_parser_lang = target_lang if target_lang != "TypeScript" else "JavaScript"
            target_parser = self.parsers[target_parser_lang]
            ir_target = target_parser.parse_source(generated_code, "test")

            if not ir_target:
                return {
                    "success": False,
                    "error": "Generated code is not parseable",
                    "quality_score": 0,
                }

            # Assess quality
            compilation = self.assessor.assess_compilation_validity(generated_code, target_lang)
            semantics = self.assessor.assess_semantic_preservation(ir_source, ir_target, source_lang, target_lang)
            idioms = self.assessor.assess_idiomatic_code(generated_code, target_lang)
            types = self.assessor.assess_type_accuracy(ir_target)

            # Calculate total quality score (out of 40)
            total_score = compilation.score + semantics.score + idioms.score + types.score
            total_max = 40
            quality_percentage = (total_score / total_max) * 100

            # Determine quality level
            if quality_percentage >= 90:
                quality_level = "Excellent"
            elif quality_percentage >= 70:
                quality_level = "Good"
            elif quality_percentage >= 50:
                quality_level = "Fair"
            else:
                quality_level = "Poor"

            return {
                "success": True,
                "quality_score": quality_percentage,
                "quality_level": quality_level,
                "metrics": {
                    "compilation": compilation,
                    "semantics": semantics,
                    "idioms": idioms,
                    "types": types,
                },
                "ir_source_funcs": len(ir_source.functions),
                "ir_target_funcs": len(ir_target.functions),
                "generated_lines": len(generated_code.split('\n')),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "quality_score": 0,
            }

    def run_full_matrix(self):
        """Test all combinations."""
        print("\n" + "="*80)
        print("TRANSLATION QUALITY ASSESSMENT - REAL-WORLD CODE PATTERNS")
        print("="*80)
        print("\nTesting 25 language combinations across 8 real-world patterns")
        print("Measuring: Compilation, Semantics, Idioms, Type Accuracy\n")

        languages = ["Python", "JavaScript", "Go", "Rust", "C#"]
        patterns = list(REAL_WORLD_PATTERNS.keys())

        # Test each combination
        total_tests = 0
        excellent_count = 0
        good_count = 0
        fair_count = 0
        poor_count = 0

        for source_lang in languages:
            for target_lang in languages:
                combo_key = f"{source_lang}→{target_lang}"
                self.results[combo_key] = []

                for pattern_name in patterns:
                    result = self.test_pattern(pattern_name, source_lang, target_lang)
                    self.results[combo_key].append((pattern_name, result))

                    if result["success"]:
                        total_tests += 1
                        level = result["quality_level"]

                        if level == "Excellent":
                            excellent_count += 1
                        elif level == "Good":
                            good_count += 1
                        elif level == "Fair":
                            fair_count += 1
                        else:
                            poor_count += 1

        # Print results
        self.print_summary(total_tests, excellent_count, good_count, fair_count, poor_count)
        self.print_detailed_results()
        self.print_gap_analysis()

    def print_summary(self, total, excellent, good, fair, poor):
        """Print summary statistics."""
        print("\n" + "="*80)
        print("OVERALL QUALITY SUMMARY")
        print("="*80)
        print(f"\nTotal translations tested: {total}")
        print(f"\nQuality Distribution:")
        print(f"  Excellent (90-100%): {excellent:3d} ({100*excellent//total if total > 0 else 0}%)")
        print(f"  Good      (70-89%):  {good:3d} ({100*good//total if total > 0 else 0}%)")
        print(f"  Fair      (50-69%):  {fair:3d} ({100*fair//total if total > 0 else 0}%)")
        print(f"  Poor      (<50%):    {poor:3d} ({100*poor//total if total > 0 else 0}%)")

        production_ready = excellent + good
        print(f"\nProduction-Ready: {production_ready}/{total} ({100*production_ready//total if total > 0 else 0}%)")

    def print_detailed_results(self):
        """Print detailed results by combination."""
        print("\n" + "="*80)
        print("DETAILED RESULTS BY LANGUAGE COMBINATION")
        print("="*80)

        for combo_key, pattern_results in sorted(self.results.items()):
            print(f"\n{combo_key}")
            print("-" * 40)

            for pattern_name, result in pattern_results:
                if result["success"]:
                    level = result["quality_level"]
                    score = result["quality_score"]

                    # Color code by level
                    if level == "Excellent":
                        icon = "🟢"
                    elif level == "Good":
                        icon = "🟡"
                    elif level == "Fair":
                        icon = "🟠"
                    else:
                        icon = "🔴"

                    print(f"  {icon} {pattern_name:25s} {score:5.1f}% ({level})")
                else:
                    print(f"  ❌ {pattern_name:25s} ERROR: {result.get('error', 'Unknown')[:30]}")

    def print_gap_analysis(self):
        """Identify specific issues across all tests."""
        print("\n" + "="*80)
        print("GAP ANALYSIS - SPECIFIC ISSUES FOUND")
        print("="*80)

        # Collect all issues
        issue_categories = {
            "compilation": [],
            "semantics": [],
            "idioms": [],
            "types": [],
        }

        for combo_key, pattern_results in self.results.items():
            for pattern_name, result in pattern_results:
                if result["success"] and "metrics" in result:
                    for metric_name, metric in result["metrics"].items():
                        if metric.issues:
                            for issue in metric.issues:
                                issue_categories[metric_name].append({
                                    "combo": combo_key,
                                    "pattern": pattern_name,
                                    "issue": issue,
                                })

        # Print issues by category
        for category, issues in issue_categories.items():
            if issues:
                print(f"\n📋 {category.upper()} Issues ({len(issues)} found):")
                print("-" * 80)

                # Group by issue type
                issue_counts = {}
                for item in issues:
                    issue_text = item["issue"]
                    if issue_text not in issue_counts:
                        issue_counts[issue_text] = []
                    issue_counts[issue_text].append(item["combo"])

                # Print sorted by frequency
                for issue_text, combos in sorted(issue_counts.items(), key=lambda x: -len(x[1])):
                    print(f"\n  • {issue_text}")
                    print(f"    Affected: {len(combos)} combination(s)")
                    if len(combos) <= 5:
                        for combo in combos:
                            print(f"      - {combo}")
                    else:
                        for combo in combos[:3]:
                            print(f"      - {combo}")
                        print(f"      ... and {len(combos)-3} more")


def main():
    """Run quality assessment."""
    tester = QualityMatrixTester()
    tester.run_full_matrix()

    return 0


if __name__ == "__main__":
    exit(main())
