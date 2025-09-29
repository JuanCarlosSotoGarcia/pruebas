import time
import sys
import csv

# ===============================
# HashSet con Linear Probing
# ===============================

class HashSet:
    def __init__(self, initial_capacity=10):
        self.capacity = initial_capacity
        self.buckets = [None] * self.capacity
        self.size = 0
        self.EMPTY = None
        self.collisions_count = 0

    def hash(self, key):
        if not isinstance(key, str):
            raise TypeError("HashSet can only contain strings")
        return sum(ord(c) for c in key) % self.capacity

    def put(self, key):
        if not isinstance(key, str):
            raise TypeError("HashSet can only contain strings")
        
        if self.size >= self.capacity * 0.75:  
            self._resize()
        
        index = self.hash(key)
        original_index = index
        
        while self.buckets[index] != self.EMPTY:
            if self.buckets[index] == key:
                return  
            self.collisions_count += 1
            index = (index + 1) % self.capacity
            if index == original_index:
                raise Exception("HashSet is full")
        
        self.buckets[index] = key
        self.size += 1

    def contains(self, key):
        if not isinstance(key, str):
            raise TypeError("HashSet can only contain strings")
        
        index = self.hash(key)
        original_index = index

        for _ in range(self.capacity):
            if self.buckets[index] == self.EMPTY:
                return False
            if self.buckets[index] == key:
                return True
            index = (index + 1) % self.capacity
            if index == original_index:
                break
        
        return False

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [self.EMPTY] * self.capacity
        self.size = 0
        self.collisions_count = 0
        
        for item in old_buckets:
            if item != self.EMPTY:
                self.put(item)

# ===============================
# HashMap con Chaining
# ===============================

class HashMap:
    def __init__(self, initial_capacity=10):
        self.capacity = initial_capacity
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        self.collisions_count = 0
        self.A = 0.618 

    def hash(self, key):
        if not isinstance(key, (int, float)):
            raise TypeError("HashMap only accepts numbers as keys")
        
        if isinstance(key, float):
            key = int(key)
        
        fractional = (key * self.A) % 1
        return int(self.capacity * fractional)

    def add(self, key, value):

        if not isinstance(key, (int, float)):
            raise TypeError("HashMap only accepts numbers as keys")
        if not isinstance(value, str):
            raise TypeError("HashMap only accepts strings as values")
        
        if self.size >= self.capacity * 0.75: 
            self._resize()
        
        index = self.hash(key)
        bucket = self.buckets[index]
     
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        if len(bucket) > 0:
            self.collisions_count += 1
        
        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        if not isinstance(key, (int, float)):
            raise TypeError("HashMap only accepts numbers as keys")
        
        index = self.hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return None

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        self.collisions_count = 0
        
        for bucket in old_buckets:
            for key, value in bucket:
                self.add(key, value)

# ===============================
# Aplicación al Dataset
# ===============================

def load_dataset(filename):
    book_titles = []
    isbn_title_pairs = []
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            
            # Asumiendo que Book-Title está en columna 2 e ISBN en columna 0
            for row in reader:
                if len(row) >= 3:
                    book_title = row[2].strip('"')
                    isbn = row[0].strip('"')
                    
                    book_titles.append(book_title)
                    isbn_title_pairs.append((isbn, book_title))
        
        return book_titles, isbn_title_pairs
    
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {filename}")
        return [], []

def test_implementations():
    print("=== Testing HashSet ===")
    hash_set = HashSet(10)
    hash_set.put("hello")
    hash_set.put("world")
    
    assert hash_set.contains("hello") == True
    assert hash_set.contains("world") == True
    assert hash_set.contains("nonexistent") == False
    
    # Test error handling
    try:
        hash_set.put(123) 
        assert False, "Expected TypeError for non-string value"
    except TypeError:
        assert True
    
    print("HashSet tests passed!")
    
    # Test HashMap
    print("\n=== Testing HashMap ===")
    hash_map = HashMap(10)
    
    # Test add y get
    hash_map.add(123, "test value")
    hash_map.add(456, "another value")
    
    assert hash_map.get(123) == "test value"
    assert hash_map.get(456) == "another value"
    assert hash_map.get(789) == None
    
    # Test error handling
    try:
        hash_map.add("invalid", "value")  
        assert False, "Expected TypeError for non-number key"
    except TypeError:
        assert True
    
    try:
        hash_map.add(123, 456)  
        assert False, "Expected TypeError for non-string value"
    except TypeError:
        assert True
    
    print("HashMap tests passed!")

def main():
  
    
    # Ejecutar pruebas
    test_implementations()
    
    # Cargar dataset
    filename = "books.csv"  
    book_titles, isbn_title_pairs = load_dataset(filename)
    
    if not book_titles:
        print("No se pudo cargar el dataset. Usando datos de ejemplo...")
        book_titles = ["Book A", "Book B", "Book C", "Book D", "Book E"]
        isbn_title_pairs = [("001", "Book A"), ("002", "Book B"), ("003", "Book C")]
    
    print(f"\nDataset cargado: {len(book_titles)} títulos, {len(isbn_title_pairs)} pares ISBN-Título")
    
    initial_capacity_hashset = int(len(book_titles) / 0.75) + 1
    initial_capacity_hashmap = int(len(isbn_title_pairs) / 0.75) + 1
    
    print("\n=== Creando HashSet ===")
    inicio = time.time()
    
    hash_set = HashSet(initial_capacity_hashset)
    for title in book_titles:
        hash_set.put(title)
    
    fin = time.time()
    tiempo_carga_hashset = fin - inicio
    
    print("\n=== Creando HashMap ===")
    inicio = time.time()
    
    hash_map = HashMap(initial_capacity_hashmap)
    for isbn, title in isbn_title_pairs:
        # Convertir ISBN a número para usar como clave
        try:
            isbn_num = int(isbn.replace("-", "").replace(" ", ""))
            hash_map.add(isbn_num, title)
        except ValueError:
            # Si no se puede convertir a número, usar hash del string
            isbn_num = sum(ord(c) for c in isbn)
            hash_map.add(isbn_num, title)
    
    fin = time.time()
    tiempo_carga_hashmap = fin - inicio
    
    # Mostrar métricas
    print("\n=== MÉTRICAS ===")
    print(f"HashSet:")
    print(f"  - Tiempo de carga: {tiempo_carga_hashset:.4f} segundos")
    print(f"  - Colisiones: {hash_set.collisions_count}")
    print(f"  - Tamaño en memoria: {sys.getsizeof(hash_set.buckets)} bytes")
    print(f"  - Elementos almacenados: {hash_set.size}")
    print(f"  - Capacidad: {hash_set.capacity}")
    print(f"  - Factor de carga real: {hash_set.size / hash_set.capacity:.2f}")
    
    print(f"\nHashMap:")
    print(f"  - Tiempo de carga: {tiempo_carga_hashmap:.4f} segundos")
    print(f"  - Colisiones: {hash_map.collisions_count}")
    print(f"  - Tamaño en memoria: {sys.getsizeof(hash_map.buckets)} bytes")
    print(f"  - Elementos almacenados: {hash_map.size}")
    print(f"  - Capacidad: {hash_map.capacity}")
    print(f"  - Factor de carga real: {hash_map.size / hash_map.capacity:.2f}")
    
    # Pruebas de búsqueda
    print("\n=== PRUEBAS DE BÚSQUEDA ===")
    
    # Búsquedas existentes
    if book_titles:
        inicio = time.time()
        found = hash_set.contains(book_titles[0])
        fin = time.time()
        print(f"Búsqueda existente en HashSet: {fin - inicio:.6f} segundos - Encontrado: {found}")
    
    if isbn_title_pairs:
        try:
            isbn_num = int(isbn_title_pairs[0][0].replace("-", "").replace(" ", ""))
            inicio = time.time()
            title = hash_map.get(isbn_num)
            fin = time.time()
            print(f"Búsqueda existente en HashMap: {fin - inicio:.6f} segundos - Título: {title}")
        except ValueError:
            pass
    
    # Búsquedas inexistentes
    inicio = time.time()
    found = hash_set.contains("Libro Inexistente XYZ123")
    fin = time.time()
    print(f"Búsqueda inexistente en HashSet: {fin - inicio:.6f} segundos - Encontrado: {found}")
    
    inicio = time.time()
    title = hash_map.get(999999999)
    fin = time.time()
    print(f"Búsqueda inexistente en HashMap: {fin - inicio:.6f} segundos - Título: {title}")

if __name__ == "__main__":
    main()