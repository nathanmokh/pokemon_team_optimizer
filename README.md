<h1> Poke-Builder </h1>
<p><i>By: Nathan Mokhtarzadeh, Jonah Mokhtarzadeh, Zachary Mokhtarzadeh</i></p>

<h2>A pokemon team builder project!</h2>
<p> The purpose of this project is to create a team builder/optimizer for pokemon. Feature suggestions are welcome, the goal is to build a system that will auto update with the newest pokemon from the PokeAPI, and be able to create the "optimal" team given certain parameters and constraints. We are using a wrapper for the Pokemon API called <a href="https://github.com/PokeAPI/pokebase">Pokebase</a> Pokebase comes with auto caching which will be a significant performance boost over using the PokeAPI directly.

<h2>Install Dependencies:</h2>
<ol>
    <li>
    <p><a href="https://www.postgresql.org/download/"> Install PostgreSQL</a> and create a database named <i>pokemon</i> hosted on localhost for development. (You can name it something else if you would like to modify the configs)</p>
    </li>
    <li>
    <p>Assuming python and pip are installed, the dependencies can be installed by cloning the repo and using the command in the main directory: 
    <br> <code> pip install -r requirements.txt </code>
    <br>
    this will ensure you have the latest versions of the dependencies being used. Remember to create a virtual environment to install the dependencies to, documentation for this can be found <a href="https://docs.python.org/3/library/venv.html">here</a>.</p>
    </li>
</ol>

<h2>Additional setup steps</h2>
<ol>
    <li>
    <p> Add your PostgreSQL password to your env, match the key with the value in <code>config/dev.yaml</code>
    </p>
    </li>
    <li>
    <p>As of writing this now there aren't a whole lot of other steps, table creation and population scripts will be stored in the repo so that should populate the db for you when setting the project up.</p>
    </li>
</ol>

<h2>Helpful Documentation:</h2>
<ul>
    <li><a href="https://pokebase.readthedocs.io/en/latest/">Pokebase Documentation</a></li>
    <li><a href="https://www.postgresql.org/docs/">PostgreSQL Documentation</a></li>
    <li><a href="https://pokeapi.co/docs/v2">PokeAPI Documentation</a></li>
</ul>