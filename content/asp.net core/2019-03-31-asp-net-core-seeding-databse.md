---
Title: ASP.NET Core seeding the database
Tags: C#, ASP.NET Core
---

It can be useful to seed the database with initial data. 
In this post we'll take a look at one way of achieving this.

## Domain model

In this example we'll use a simple domain model.

```csharp
class Person
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public int Age { get; set; }
}
```

## DbContext

Before seeding the database we have to let `DbContext` know about our `Person` model.

!!! info
    This post won't go into any detail about `DbContext`. 
    If you would like to have more information you can read about it on [Microsoft Docs about Configuring a DbContext](https://docs.microsoft.com/en-us/ef/core/miscellaneous/configuring-dbcontext)

This is a very simple `DbContext` implementation for this example.

```csharp
public class MyDbContext : DbContext
{
    public MyDbContext() : base()
    {
    }

    public MyDbContext(DbContextOptions options) : base(options)
    {
    }

    public virtual DbSet<Person> People { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Person>().ToTable("People");
    }
}
```

## Connection string and building the database

Without going into too much detail, I'll show you how to setup the connection string and build the database.

First you need to set the connection string in `appsettings.json`. 

```json
{
    "ConnectionStrings": {
        "DefaultConnection":  "Server=(localdb)\\mssqllocaldb;Database=MyDatabase;Trusted_Connection=True;MultipleActiveResultSets=true" 
    } 
}
```

Next you need to add `MyDbContext` to the `ConfigureServices()` method of the `Startup()` class.

```csharp
public void ConfigureServices(IServiceCollection services)
{
    // Get the connection string from appsettings.json
    var connection = Configuration.GetConnectionString("DefaultConnection") ?? "testingconnection";

    // Add MyDbContext to the service collection and tell it to use Sql Server as a database provider
    services.AddDbContext<MyDbContext>(options =>
        options.UseSqlServer(connection)
    );

    // Some other settings
}
```

Finally you can create the migrations and update the database

```ps1
> dotnet ef migrations add AddPersonModel
info: Microsoft.EntityFrameworkCore.Infrastructure[10403]
      Entity Framework Core 2.2.1-servicing-10028 initialized 'MyDbContext' using provider 'Microsoft.EntityFrameworkCore.SqlServer' with options: None
Done. To undo this action, use 'ef migrations remove'
> dotnet ef database update
info: Microsoft.EntityFrameworkCore.Infrastructure[10403]
      Entity Framework Core 2.2.1-servicing-10028 initialized 'MyDbContext' using provider 'Microsoft.EntityFrameworkCore.SqlServer' with options: None
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (322ms) [Parameters=[], CommandType='Text', CommandTimeout='60']
      CREATE DATABASE [MyDatabase];
... Some more output
```

## DbInitializer

The responsibility of the `DbInitializer` class is to initialize data in the database.

```csharp
public class DbInitializer
{
    public static void Initialize(MyDbContext context, IServiceProvider services)
    {
        // Get a logger
        var logger = services.GetRequiredService<ILogger<DbInitializer>>();

        // Make sure the database is created
        // We already did this in the previous step
        context.Database.EnsureCreated();

        if (context.Authors.Any())
        {
            logger.LogInformation("The database was already seeded");
            return;
        }

        logger.LogInformation("Start seeding the database.");

        var person = new Person
        {
            FirstName = "Johan",
            LastName = "Vergeer",
            Age = 32
        };

        context.People.Add(person);
        context.SaveChanges();

        logger.LogInformation("Finished seeding the database.");
    }
}
```

I think this is pretty self explanatory, but I'll add some explanation. 
The static `Initialize()` method takes a `MyDbContext` and an `IServiceProvider` instance as input parameters. 
We'll see in the next step how these are passed in. 
Especially in these setup methods I prefer to log too much over too little. 
They won't be called more then once in the lifetime of the application, 
so they won't clutter your log very much, and it gives us some insights that have proven 
to be very useful to me.

We just create one `Person` object, which is added to `MyDbContext`, 
after which `MyDbContext` saves the `Person` to the database.

## Use DbInitializer

`DbInitializer` should run after the application has started, and before the user starts using it. 
Because we also want to be able to seed a database with other data while testing, 
the database can't be initialized in `Startup`. 
Therefore we put the initialization in the `Program` class, right after the host is built. 

```csharp
public class Program
{
    public static void Main(string[] args)
    {
        var host = CreateWebHostBuilder(args).Build();

        SeedDatabase(host);

        host.Run();
    }

    public static IWebHostBuilder CreateWebHostBuilder(string[] args) =>
        WebHost.CreateDefaultBuilder(args)
            .UseStartup<Startup>();

    private static void SeedDatabase(IWebHost host)
    {
        using (var scope = host.Services.CreateScope())
        {
            var services = scope.ServiceProvider;
            try
            {
                var context = services.GetRequiredService<MyDbContext>();

                DbInitializer.Initialize(context, services);
            }
            catch (Exception ex)
            {
                var logger = services.GetRequiredService<ILogger<Program>>();
                logger.LogError("An error occurred while seeding the database");
            }
        }
    }
}
```

As you can see, we can get `MyDbContext` from the services collection because we already ran `Startup`.
Here we pass the `context` and the `IServiceProvider` instance, `services`, to the `Initialize()` method of `DbInitializer`, where
`context` is used to add and save the `Person` instance to the database, and `services` is used to get the `ILogger` instance.

# Run the application

Now when we run the application for the first time, the data is seeded to the database.
