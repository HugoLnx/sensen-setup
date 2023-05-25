
# Unity Conventions #

## Folder Naming Convention
* Use pascal case. (eg. PhysicsMaterials)
* Use upper case wrapped in square brackets for debug folders. (eg. \[JOHN_SANDBOX])

## Assets Filename Conventions
### camelCase with `_` for grouping.
```
weapons_sword_short.png
weapons_gun_machineGun.png
weapons_gun_miniGun.png
weapons_flameThrower.png

// Extensions always in lower case!!!
```


## GameObjects Naming Convention
* Use pascal case. (eg. AudioManager)
* Use upper case wrapped in square brackets for debug objects. (eg. \[DEBUG_MOUNTAIN])


# Code Styling Conventions #

## Decrease Code Density
### Spaces after `;`, `,` and flow control keywords
```C#
for (int i = 0; i < 100; i++)
{
    // ...
}
```

### Spaces around comparison, attribution or arithmetic signs
```C#
bool isTheTruth = (22 + 20) == (30 + 12);
```

### Spaces inside inline curly brackets
```C#
public bool IsTheTruth { get; private set; } = 42;
new Dictionary<string, int>() {
    { "The Truth", 42 },
    { "Not The Truth", 17 },
};
```

## Naming
### Pascal Case
Use it on...
* Classes
* Methods
* Properties
* Constants
* Delegates
* Events
* Read-Only Static Fields
* Enums (also must be in singular)
* Namespaces
```C#
namespace SensenToolkit.Math.TwoDimensions
{
    public class Line2D
    {
        #region Nested
        public enum Fruit
        {
            Apple,
            Orange,
            Guava,
        }
        #endregion

        #region Static
        public const int TheTruth = 42;
        private const int TheTruth2 = 42;
        public static readonly string TheTruthString = "42";
        private static readonly string TheTruthString2 = "42";
        #endregion

        #region Properties
        public bool IsTheTruth => TheTruth == TheTruth;
        #endregion

        #region Delegates
        public delegate void TriggeredHandler();
        public event TriggeredHandler OnTriggered;
        #endregion
    }
}
```

### CamelCase on fields and local variables
```C#
// Private fields are prefixed with "_"
private float _theTruth;

// Mutable private fields are prefixed with "s_"
private static float s_theTruth;

// Local variables are not prefixed
public FindTheTruth(bool poluteTheTruth = false)
{
    var baseTruth = 42f;
    return baseTruth + (poluteTheTruth ? 0.0001f : 0f);
}
```

## Implicit typing via `var` keyword
### Use it when...
```C#
// It's an obvious type
var person = new Person();
var item = Factory.Create<Item>();
var player = GetComponent<Player>();
```

### Do NOT use it when...
```C#
// Dealing with numbers
long x = 1L + 5L;
ulong b = bitboard & mask;
int y = 20;

// Getting value from method calls (except GetComponents and derivatives)
List<Item> items = GetItems();

// for or foreach loops
for (int i = 0; i < 100; i++)
{
    // ...
}

foreach (Line line in lines)
{
    // ...
}
```

## Code length guidelines
* Line Width: 120 characters (Max)
* Class Size: 100 lines (Ideal)
* Method Size: 25 lines (Ideal)

## Class Organization
The classe must be organized into the following regions:
1. Nested : Nested classes, enums and structs
2. Static : Constants and static fields and properties
    - Constants and static readonly fields first
    - Properties at the end
3. Fields : Instance fields
    - Serialized fields first
4. Properties : Instance properties
    - Public above private
5. Delegates : Events and delegates
    - If the event declaration uses a delegates, declare it above the event
    - Other delegates below all events
6. Init : Constructors, Awake, Start, factory methods and similar.
7. Exposed : What the class are exposing to others
    - Static methods above instance
    - Public above protected methods
    - Includes virtual/abstract methods
8. Lifecycle : Lifecycle methods (OnEnable, Update and other unity or non-unity callbacks)
    - Starting methods first (OnEnable, OnEnter, etc)
    - Finalizing methods last (OnDisable, OnDestroy, OnExit, etc)
9. Private : Private static and instance methods
    - Instance methods first

Don't let empty regions hanging around, delete them.
