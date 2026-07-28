# Teori — Tree, Heap ve Graph

## 1. Tree

Tree, düğümler ve yönlü ebeveyn-çocuk ilişkilerinden oluşan hiyerarşik bir veri yapısıdır. Root en üst düğümdür; leaf düğümlerin çocuğu yoktur. Bir düğümün depth değeri root'tan uzaklığını, height değeri ise en uzak leaf'e olan mesafeyi ifade eder.

Binary tree'de her düğümün en fazla iki çocuğu bulunur. Binary search tree'de sol alt ağaçtaki değerler düğümden küçük, sağ alt ağaçtaki değerler büyüktür. Dengeli bir BST'de arama ve ekleme ortalama `O(log n)`, kötü durumda `O(n)` olabilir.

Traversal türleri:

- Preorder: node, left, right
- Inorder: left, node, right
- Postorder: left, right, node
- Level-order: seviyeler boyunca BFS

## 2. Heap

Heap, complete binary tree düzenini koruyan ve heap property uygulayan bir yapıdır. Min-heap'te parent değeri çocuklarından küçük veya eşittir. Root her zaman minimum değeri taşır.

Python'da `heapq` min-heap sağlar. Ekleme ve minimum elemanı çıkarma `O(log n)`, minimumu görme `O(1)` maliyetlidir. Heap; task scheduling, top-k seçimi ve best-first search için uygundur.

## 3. Graph

Graph, vertex ve edge kümelerinden oluşur. Yönlü/yönsüz ve ağırlıklı/ağırlıksız olabilir. Sparse graph'larda adjacency list genellikle adjacency matrix'ten daha az bellek kullanır.

### BFS

BFS queue kullanır ve düğümleri katman katman gezer. Ağırlıksız graph'ta en kısa kenar sayılı yolu bulabilir. Karmaşıklığı adjacency list ile `O(V + E)` olur.

### DFS

DFS stack veya recursion kullanır ve bir yolu mümkün olduğunca derin takip eder. Connected component, cycle detection ve topological ordering gibi problemlerde kullanılır. Karmaşıklığı `O(V + E)` olur.

## 4. Topological ordering

Yönlü ve döngüsüz graph (DAG) için, her `u -> v` kenarında `u` düğümünün `v` düğümünden önce geldiği sıralamadır. AI pipeline bağımlılıkları ve iş akışı orkestrasyonu için kullanılabilir. Döngü varsa geçerli topological ordering yoktur.

## 5. AI mühendisliği bağlantıları

- Decision tree ve model hiyerarşileri: tree
- Öncelikli inference talepleri ve top-k skorlar: heap
- Agent tool dependency ve workflow DAG'leri: graph
- Knowledge graph ve veri lineage: graph
- Beam search adaylarının yönetimi: heap

Doğru veri yapısı seçimi yalnızca teorik karmaşıklığa değil; veri boyutu, güncelleme sıklığı, bellek kullanımı ve erişim desenine de bağlıdır.