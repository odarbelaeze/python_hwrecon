#include <fstream>

using namespace std;

int main(int argc, char const *argv[])
{
    ifstream data;
    ifstream labels;
    ofstream char_recon;

    int num_instances = 2600;
    int num_character = 1600;

    float val;

    for (int i = 0; i < num_instances; ++i)
    {
        labels >> val;
        ofstream << (int) val << "    ";
        for (int j = 0; j < num_character; ++j)
        {
            data >> val;
            ofstream << j + 1 << ":" << (int)val << " ";
        }
        ofstream << endl;
    }

    return 0;
}