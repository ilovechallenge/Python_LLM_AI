Welcome to LMQL
===================================

**LMQL** (Language Model Query Language) is a programming language for large language model interaction. 
It facilitates LLM interaction by combining the benefits of natural language prompting with the expressiveness 
of Python. With only a few lines of LMQL code, users can express advanced, multi-part and tool-augmented LM queries, 
which then are optimized by the LMQL runtime to run efficiently as part of the LM decoding loop.

LMQL is a research project by the `Secure,  Reliable, and Intelligent Systems Lab <https://www.sri.inf.ethz.ch/>`_ at ETH Zürich.

Quick Start
-----------

To get started, check out the :doc:`quickstart`. We provide the following resources and options to get started with LMQL:

.. raw:: html

    <div class="getting-started-options">
      <div class="columns is-getting-started">
        <div class="column getting-started">
          <h2>Explore LMQL</h2>
          <a class="primary" href="https://lmql.ai/playground">
            Playground IDE
          </a>
          <a href="quickstart.html">
            🚀 Getting Started Guide
          </a>
          <a href="https://github.com/eth-sri/lmql">
            GitHub Repo
          </a>
        </div>

        <div class="column getting-started">
          <h2>Run Locally</h2>
          <div class="cmd"> 
              pip install lmql
          </div> 
          To run LMQL locally, read the <span><a href="quickstart.html">Installation Instructions</a> section of the documentation</span>.
        </div>
      </div>
    </div>

Contents
--------

.. toctree::
  :maxdepth: 1

  quickstart
  installation
  Playground IDE <https://lmql.ai/playground>

.. toctree::
   :maxdepth: 1
   :caption: 📖 LMQL Language 
   
   language/scripted_prompts.md
   language/constraints.md
   language/decoders.md
   language/models.md
   language/functions.md
   
.. toctree::
    :maxdepth: 1
    :caption: 🔗 Python Interoperability
    
    python/python.ipynb
    python/langchain.ipynb
   
.. toctree:
    :maxdepth: 2
    :caption: Development
    dev-setup
